import requests
from pathlib import Path
from io import BytesIO
import sys

URL = "https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf"

try:
    from PyPDF2 import PdfReader
except Exception as e:
    PdfReader = None
    print("PyPDF2 import failed:", e)

try:
    import pdfplumber
except Exception:
    pdfplumber = None


def fetch():
    print("Fetching:", URL)
    try:
        resp = requests.get(URL, timeout=30)
    except Exception as e:
        print("Request failed:", e)
        return None
    print("Status:", resp.status_code)
    headers = resp.headers
    for k in ("Content-Type", "Content-Length", "Content-Disposition"):
        if k in headers:
            print(f"{k}: {headers[k]}")
    return resp


def save(resp):
    base = Path(__file__).resolve().parent
    out = base / "debug_20260601632081678.pdf"
    out.write_bytes(resp.content)
    print("Saved to:", out)
    return out


def try_pypdf2(content: bytes):
    if PdfReader is None:
        print("PyPDF2 not available")
        return
    try:
        reader = PdfReader(BytesIO(content))
        n = len(reader.pages)
        print("PyPDF2 pages:", n)
        text = []
        for i, p in enumerate(reader.pages[:5]):
            try:
                t = p.extract_text() or ""
            except Exception as e:
                t = f"<error extracting page: {e}>"
            text.append(t)
        joined = "\n\n".join(text)
        print("Sample text (first 1000 chars):")
        print(joined[:1000])
    except Exception as e:
        print("PyPDF2 failed:", repr(e))


def try_pdfplumber(path: Path):
    if pdfplumber is None:
        print("pdfplumber not available")
        return
    try:
        with pdfplumber.open(path) as pdf:
            print("pdfplumber pages:", len(pdf.pages))
            texts = []
            for p in pdf.pages[:5]:
                try:
                    texts.append(p.extract_text() or "")
                except Exception as e:
                    texts.append(f"<error:{e}>")
            joined = "\n\n".join(texts)
            print("Sample text (first 1000 chars):")
            print(joined[:1000])
    except Exception as e:
        print("pdfplumber failed:", e)


def main():
    resp = fetch()
    if resp is None:
        sys.exit(1)
    if resp.status_code != 200:
        print("Non-200 status, aborting")
        sys.exit(2)

    out = save(resp)
    try_pypdf2(resp.content)
    try_pdfplumber(out)


if __name__ == '__main__':
    main()
