import importlib
import sys

def available(name):
    return importlib.util.find_spec(name) is not None

print('PyPDF2:', available('PyPDF2'))
print('pdfplumber:', available('pdfplumber'))
print('pytesseract:', available('pytesseract'))
print('pdf2image:', available('pdf2image'))
print('PIL (Pillow):', available('PIL'))

try:
    import pytesseract
    try:
        print('tesseract version:', pytesseract.get_tesseract_version())
    except Exception as e:
        print('tesseract binary error:', e)
except Exception as e:
    print('pytesseract import error:', e)

try:
    from pdf2image import convert_from_bytes
    print('pdf2image import success')
except Exception as e:
    print('pdf2image import error:', e)

sys.exit(0)
