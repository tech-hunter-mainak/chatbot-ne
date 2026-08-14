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
else:
    # configure tesseract binary if not on PATH
    import os
    for c in [r"C:\Program Files\Tesseract-OCR\tesseract.exe", r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"]:
        if os.path.exists(c):
            try:
                pytesseract.pytesseract.tesseract_cmd = c
                print('Configured pytesseract.tesseract_cmd ->', c)
                break
            except Exception:
                pass
try:
    from pdf2image import convert_from_bytes
except Exception:
    convert_from_bytes = None
try:
    from PIL import Image
except Exception:
    Image = None
try:
    import pypdfium2 as pdfium
except Exception:
    pdfium = None


def extract_pdf_bytes(content: bytes):
    texts = []
    print('extract_pdf_bytes: start')
    if PdfReader is not None:
        print('extract_pdf_bytes: trying PyPDF2')
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
        except Exception as e:
            print('PyPDF2 error:', e)

    if (not texts or all(not t.strip() for t in texts)) and pdfplumber is not None:
        print('extract_pdf_bytes: trying pdfplumber')
        try:
            with pdfplumber.open(BytesIO(content)) as pdf:
                for p in pdf.pages:
                    try:
                        t = p.extract_text() or ''
                    except Exception:
                        t = ''
                    texts.append(t)
        except Exception as e:
            print('pdfplumber error:', e)

    # If still empty, try OCR conversion to images
    print('extract_pdf_bytes: after pdfplumber, texts count=', len(texts))
    if (not texts or all(not t.strip() for t in texts)) and pytesseract is not None:
        print('extract_pdf_bytes: trying OCR (pytesseract)')
        # try pypdfium2 fallback first (faster and doesn't require poppler)
        print('extract_pdf_bytes: pypdfium2 available=', pdfium is not None)
        if pdfium is not None and Image is not None:
            print('extract_pdf_bytes: trying pypdfium2')
            try:
                from tempfile import NamedTemporaryFile

                with NamedTemporaryFile(delete=False, suffix='.pdf') as tf:
                    tf.write(content)
                    tmp = tf.name
                doc = pdfium.PdfDocument(tmp)
                ocr_texts = []
                for i in range(min(3, len(doc))):
                    try:
                        page = doc.get_page(i)
                        # prefer render_topil if available
                        if hasattr(page, 'render_topil'):
                            pil = page.render_topil(scale=2)
                        else:
                            renderer = page.render(scale=2)
                            if hasattr(renderer, 'to_pil'):
                                pil = renderer.to_pil()
                            elif hasattr(renderer, 'as_pil'):
                                pil = renderer.as_pil()
                            else:
                                pil = None
                                print('Renderer has no to_pil/as_pil')
                        if pil is not None:
                            t = pytesseract.image_to_string(pil)
                        else:
                            t = ''
                        try:
                            page.close()
                        except Exception:
                            pass
                    except Exception as e:
                        print('page OCR error:', e)
                        t = ''
                    ocr_texts.append(t)
                try:
                    doc.close()
                except Exception:
                    pass
                if any(t.strip() for t in ocr_texts):
                    return '\n\n'.join(t for t in ocr_texts if t)
            except Exception as e:
                print('OCR error (pypdfium2):', e)

        # try pdf2image/poppler next
        print('extract_pdf_bytes: pdf2image available=', convert_from_bytes is not None, 'PIL available=', Image is not None)
        if convert_from_bytes is not None and Image is not None:
            print('extract_pdf_bytes: trying pdf2image')
            try:
                images = convert_from_bytes(content, first_page=1, last_page=3)
                ocr_texts = []
                for img in images:
                    try:
                        if not isinstance(img, Image.Image):
                            img = Image.fromarray(img)
                        t = pytesseract.image_to_string(img)
                    except Exception as e:
                        print('pdf2image page OCR error:', e)
                        t = ''
                    ocr_texts.append(t)
                return '\n\n'.join(t for t in ocr_texts if t)
            except Exception as e:
                print('OCR error (pdf2image):', e)

    return '\n\n'.join(t for t in texts if t)


def main():
    if len(sys.argv) < 2:
        print('Usage: debug_fetch_url.py <url>')
        sys.exit(1)
    url = sys.argv[1]
    print('Fetching', url)
    r = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
    print('Status', r.status_code)
    if r.status_code != 200:
        print('Non-200, abort')
        sys.exit(2)
    ct = r.headers.get('Content-Type', '')
    print('Content-Type:', ct)
    if 'application/pdf' in ct or url.lower().endswith('.pdf'):
        text = extract_pdf_bytes(r.content)
        if text and text.strip():
            out_dir = Path(__file__).resolve().parent.parent / 'knowledge' / 'en'
            out_dir.mkdir(parents=True, exist_ok=True)
            fname = out_dir / (url.split('/')[-1].replace('.pdf','') + '.txt')
            fname.write_text(text, encoding='utf-8')
            print('Saved extracted text to', fname)
        else:
            print('No text extracted')
    else:
        print('Not a PDF (Content-Type:', ct, ')')


if __name__ == '__main__':
    main()
