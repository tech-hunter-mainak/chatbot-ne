import importlib, shutil
mods = ['PyPDF2','pdfplumber','pytesseract','pdf2image','PIL']
for m in mods:
    print(m, 'installed' if importlib.util.find_spec(m) else 'missing')
print('tesseract:', shutil.which('tesseract'))
print('pdftoppm:', shutil.which('pdftoppm'))
