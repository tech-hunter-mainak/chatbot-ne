"""Ingest web pages into the local knowledge store.

This script can fetch URLs directly or use a simple DuckDuckGo search to collect
text content and save it as `.txt` files under `backend/knowledge/<lang>/`.

After ingestion, run `python scripts/build_index.py` to rebuild the FAISS index.
"""

import argparse
import hashlib
import html
import os
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from dotenv import load_dotenv
from html.parser import HTMLParser

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
MAX_CHUNK_SIZE = 12000
CHUNK_OVERLAP = 400


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_ignored = False
        self._texts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._in_ignored = True
        elif tag in {"p", "br", "div", "li", "section", "article", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._texts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"}:
            self._in_ignored = False
        elif tag in {"p", "div", "li", "section", "article", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._texts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._in_ignored:
            return
        text = data.strip()
        if text:
            self._texts.append(text)

    def get_text(self) -> str:
        text = " ".join(self._texts)
        text = html.unescape(text)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n{2,}", "\n\n", text)
        return text.strip()


def safe_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    safe_path = re.sub(r"[^A-Za-z0-9_-]", "_", path)
    if len(safe_path) > 100:
        safe_path = safe_path[:100]
    if not safe_path:
        safe_path = "page"
    filename = f"{parsed.netloc}_{safe_path}.txt"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{filename[:-4]}_{digest}.txt"


def extract_text_from_html(html_content: str) -> str:
    parser = TextExtractor()
    parser.feed(html_content)
    return parser.get_text()


def fetch_url(url: str, timeout: int = 15) -> str | None:
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return None
        return extract_text_from_html(response.text)
    except requests.RequestException:
        return None


def call_ollama(messages: list[dict[str, str]]) -> str | None:
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={"model": LLM_MODEL, "messages": messages, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()
    except (requests.RequestException, KeyError):
        return None


def chunk_text(text: str, size: int = MAX_CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = " ".join(text.split())
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def extract_relevant_info(text: str, url: str, lang: str) -> str | None:
    system_prompt = (
        "You are an assistant that extracts the most relevant information from a web page. "
        "Return only the concise, factual, and useful content from the page. "
        "Do not include navigation, ads, menus, or unrelated boilerplate. "
        "Return plain text only."
    )
    user_prompt = (
        f"URL: {url}\n"
        f"Language code: {lang}\n\n"
        "Page text:\n"
        f"{text}\n\n"
        "Provide a concise summary containing only the relevant facts from this page."
    )
    return call_ollama([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])


def summarize_large_text(text: str, url: str, lang: str) -> str | None:
    if len(text) <= MAX_CHUNK_SIZE:
        return extract_relevant_info(text, url, lang)

    chunks = chunk_text(text)
    chunk_summaries: list[str] = []
    for idx, chunk in enumerate(chunks, start=1):
        summary = extract_relevant_info(
            chunk,
            url,
            lang,
        )
        if summary:
            chunk_summaries.append(f"Chunk {idx}: {summary}")

    if not chunk_summaries:
        return None

    combined_text = "\n\n".join(chunk_summaries)
    system_prompt = (
        "You are an assistant that merges chunk summaries into a single concise output. "
        "Keep only the most important, non-redundant facts."
    )
    user_prompt = (
        f"URL: {url}\n"
        f"Language code: {lang}\n\n"
        "Here are chunk summaries from the same page:\n"
        f"{combined_text}\n\n"
        "Combine them into one concise summary containing the relevant information only."
    )
    return call_ollama([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])


def parse_search_results(html_content: str) -> list[str]:
    urls: list[str] = []
    for match in re.finditer(r'<a[^>]+href="/l/\?kh=-1&uddg=(https?%3A%2F%2F[^"]+)"', html_content):
        encoded = match.group(1)
        url = requests.utils.unquote(encoded)
        urls.append(url)
    if not urls:
        for match in re.finditer(r'<a[^>]+href="(https?://[^"]+)"', html_content):
            url = match.group(1)
            if "duckduckgo.com" not in url:
                urls.append(url)
    return list(dict.fromkeys(urls))


def search_duckduckgo(query: str, max_results: int = 5) -> list[str]:
    params = {
        "q": query,
        "t": "h_",
        "ia": "web",
    }
    try:
        response = requests.get("https://duckduckgo.com/html/", params=params, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException:
        return []
    urls = parse_search_results(response.text)
    return urls[:max_results]


def save_text(lang_dir: Path, url: str, text: str) -> Path:
    source = safe_filename(url)
    path = lang_dir / source
    path.write_text(text, encoding="utf-8")
    return path


def load_urls_from_file(file_path: Path) -> list[str]:
    if not file_path.exists():
        return []
    return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]


def ingest_urls(lang_dir: Path, urls: Iterable[str], max_pages: int | None = None) -> list[Path]:
    saved_files: list[Path] = []
    for count, url in enumerate(urls, start=1):
        if max_pages is not None and count > max_pages:
            break
        text = fetch_url(url)
        if not text:
            continue
        relevant = summarize_large_text(text, url, lang_dir.name)
        if not relevant:
            relevant = text
        saved_files.append(save_text(lang_dir, url, relevant))
    return saved_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest web pages into backend/knowledge/<lang>/")
    parser.add_argument("--lang", required=True, help="Language code to store the ingested files")
    parser.add_argument("--urls", nargs="*", default=[], help="One or more page URLs to ingest")
    parser.add_argument("--source-file", type=Path, help="Text file with one URL per line")
    parser.add_argument("--query", help="DuckDuckGo search query to discover pages")
    parser.add_argument("--max-pages", type=int, default=0, help="Maximum number of pages to ingest (0 = no limit)")
    parser.add_argument("--max-results", type=int, default=5, help="Maximum search results to use for query ingestion")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    knowledge_dir = base_dir / "knowledge"
    lang_dir = knowledge_dir / args.lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    urls: list[str] = []
    if args.source_file:
        urls.extend(load_urls_from_file(args.source_file))
    urls.extend(args.urls)

    if args.query:
        urls.extend(search_duckduckgo(args.query, max_results=args.max_results))

    urls = [url for url in urls if url.strip()]
    if not urls:
        print("No URLs found. Provide --urls, --source-file, or --query.")
        return

    max_pages = args.max_pages if args.max_pages > 0 else None
    page_count = args.max_pages if args.max_pages > 0 else "all"
    print(f"Ingesting up to {page_count} pages into {lang_dir}...")
    saved = ingest_urls(lang_dir, urls, max_pages=max_pages)

    if not saved:
        print("No pages were ingested.")
        return

    print("Saved files:")
    for path in saved:
        print(f"- {path}")
    print("Done. Run `python scripts/build_index.py` to update the FAISS index.")


if __name__ == "__main__":
    main()
