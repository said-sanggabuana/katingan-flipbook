import fitz
import os

filepath = 'docs/1_dokumen kajian desa karuing final layout.pdf'
doc = fitz.open(filepath)
print('Optimizing with deflate_images...')
try:
    doc.save(filepath + '.opt.pdf', garbage=4, deflate=True, deflate_images=True, deflate_fonts=True)
except Exception as e:
    print(f"Failed with advanced options: {e}")
doc.close()
print(f"Size: {os.path.getsize(filepath + '.opt.pdf') / (1024*1024):.2f} MB")
