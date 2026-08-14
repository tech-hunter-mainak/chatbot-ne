import requests
from io import BytesIO
from pathlib import Path

URL = 'https://www.nits.ac.in/storage/Feestructure/Feestructure_6a15a5b6d6c231779803574.pdf'

try:
    import pypdfium2 as pdfium
except Exception as e:
    print('pypdfium2 import error', e)
    pdfium = None
try:
    from PIL import Image
except Exception as e:
    print('PIL import error', e)
    Image = None
try:
    import pytesseract
except Exception as e:
    print('pytesseract import error', e)
    pytesseract = None

# If tesseract binary isn't on PATH, try common install locations and configure pytesseract
if pytesseract is not None:
    import os
    candidates = [r"C:\Program Files\Tesseract-OCR\tesseract.exe", r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"]
    for c in candidates:
        if os.path.exists(c):
            pytesseract.pytesseract.tesseract_cmd = c
            print('Configured pytesseract.tesseract_cmd ->', c)
            break

def main():
    print('Fetching', URL)
    r = requests.get(URL, timeout=30, headers={'User-Agent':'Mozilla/5.0'})
    print('Status', r.status_code)
    if r.status_code != 200:
        return
    if pdfium is None:
        print('pypdfium2 not available')
        return
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(delete=False, suffix='.pdf') as tf:
        tf.write(r.content)
        tmp = tf.name
    print('Saved tmp pdf', tmp)
    try:
        doc = pdfium.PdfDocument(tmp)
        print('Pages:', len(doc))
        page = doc.get_page(0)
        print('Page object methods:', [m for m in dir(page) if not m.startswith('_')])
        # try available render methods
        saved = False
        if hasattr(page, 'render_topil'):
            pil = page.render_topil(scale=2)
            out = Path(__file__).resolve().parent / 'page0.png'
            pil.save(out)
            print('Saved image', out)
            saved = True
            page.close()
        else:
            print('render_topil not available on page')
            try:
                renderer = page.render(scale=2)
                print('Renderer methods:', [m for m in dir(renderer) if not m.startswith('_')])
                if hasattr(renderer, 'to_pil'):
                    pil = renderer.to_pil()
                    out = Path(__file__).resolve().parent / 'page0.png'
                    pil.save(out)
                    print('Saved image via renderer.to_pil', out)
                    saved = True
                elif hasattr(renderer, 'as_pil'):
                    pil = renderer.as_pil()
                    out = Path(__file__).resolve().parent / 'page0.png'
                    pil.save(out)
                    print('Saved image via renderer.as_pil', out)
                    saved = True
                else:
                    print('Renderer has no to_pil/as_pil methods')
                try:
                    renderer.close()
                except Exception:
                    pass
                page.close()
            except Exception as e:
                print('page.render error:', e)
        doc.close()
        if pytesseract is not None and saved:
            print('Running OCR...')
            txt = pytesseract.image_to_string(pil)
            print('OCR sample:', txt[:1000])
    except Exception as e:
        print('pdfium render error', e)

if __name__ == '__main__':
    main()
