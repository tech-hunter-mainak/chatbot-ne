import requests
from pathlib import Path
from urllib.parse import urlparse
from io import BytesIO

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    import pdfplumber
except Exception:
    pdfplumber = None


URL = "https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf"


def safe_filename(url: str) -> str:
    p = urlparse(url)
    name = (p.path.split('/')[-1] or 'doc').replace('.pdf', '')
    return f"{p.netloc}_{name}.txt"


def extract_text_from_pdf_bytes(content: bytes) -> str | None:
    texts = []
    if PdfReader is not None:
        try:
            try:
                reader = PdfReader(content)
            except Exception:
                reader = PdfReader(BytesIO(content))
            for page in reader.pages:
                try:
                    t = page.extract_text() or ''
                except Exception:
                    t = ''
                if t:
                    texts.append(t)
        except Exception:
            texts = []

    if (not texts or all(not t.strip() for t in texts)) and pdfplumber is not None:
        try:
            with pdfplumber.open(BytesIO(content)) as pdf:
                for p in pdf.pages:
                    try:
                        t = p.extract_text() or ''
                    except Exception:
                        t = ''
                    if t:
                        texts.append(t)
        except Exception:
            pass

    full = "\n\n".join(t for t in texts if t)
    return full.strip() if full.strip() else None


def main():
    out_dir = Path(__file__).resolve().parent.parent / 'knowledge' / 'en'
    out_dir.mkdir(parents=True, exist_ok=True)
    print('Downloading', URL)
    r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    print('Status', r.status_code, 'len', len(r.content))
    text = extract_text_from_pdf_bytes(r.content)
    if not text:
        print('No text extracted')
        return
    filename = safe_filename(URL)
    path = out_dir / filename
    path.write_text(text, encoding='utf-8')
    print('Saved to', path)


if __name__ == '__main__':
    main()
