from pypdf import PdfReader, PdfWriter
import os

filepath = 'docs/1_dokumen kajian desa karuing final layout.pdf'
print(f"Original Size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")

reader = PdfReader(filepath)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

# pypdf can try to reduce image quality
for page in writer.pages:
    page.compress_content_streams()

with open(filepath + '.pypdf.pdf', 'wb') as f:
    writer.write(f)

print(f"New Size: {os.path.getsize(filepath + '.pypdf.pdf') / (1024*1024):.2f} MB")
