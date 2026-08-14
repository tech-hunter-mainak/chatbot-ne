import sys
from pathlib import Path
from io import BytesIO
import requests

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None
try:
    import pdfplumber
except Exception:
    pdfplumber = None
try:
    import pytesseract
except Exception:
    pytesseract = None
try:
    from pdf2image import convert_from_bytes
except Exception:
    convert_from_bytes = None
try:
    from PIL import Image
except Exception:
    Image = None


def try_extract(content: bytes):
    texts = []
    if PdfReader is not None:
        try:
            try:
                reader = PdfReader(content)
            except Exception:
                reader = PdfReader(BytesIO(content))
            for p in reader.pages:
                try:
                    t = p.extract_text() or ''
                except Exception:
                    t = ''
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
                    texts.append(t)
        except Exception:
            pass

    joined = "\n\n".join(t for t in texts if t and t.strip())
    if joined.strip():
        return joined

    # OCR fallback
    if pytesseract is not None and convert_from_bytes is not None and Image is not None:
        try:
            imgs = convert_from_bytes(content)
            ocr = []
            for img in imgs[:5]:
                try:
                    if not isinstance(img, Image.Image):
                        img = Image.fromarray(img)
                    txt = pytesseract.image_to_string(img) or ''
                except Exception:
                    txt = ''
                ocr.append(txt)
            joined_ocr = "\n\n".join(t for t in ocr if t and t.strip())
            if joined_ocr.strip():
                return joined_ocr
        except Exception as e:
            print('OCR failed:', e)
    return None


def main():
    if len(sys.argv) < 2:
        print('Usage: debug_pdf_fetch_url.py <url>')
        sys.exit(1)
    url = sys.argv[1]
    print('Fetching', url)
    r = requests.get(url, timeout=30, headers={'User-Agent':'Mozilla/5.0'})
    print('Status', r.status_code)
    if r.status_code != 200:
        print('Bad status')
        sys.exit(2)
    text = try_extract(r.content)
    if not text:
        print('No text extracted')
        sys.exit(3)
    sample = text[:2000]
    print('Sample output:')
    print(sample)
    out = Path(__file__).resolve().parent.parent / 'knowledge' / 'en'
    out.mkdir(parents=True, exist_ok=True)
    fname = url.split('/')[-1].replace('.pdf','') + '.txt'
    path = out / fname
    path.write_text(text, encoding='utf-8')
    print('Saved to', path)

if __name__ == '__main__':
    main()
