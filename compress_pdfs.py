import os
from pypdf import PdfReader, PdfWriter

def compress_pypdf(filepath):
    print(f"Original {filepath}: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
    reader = PdfReader(filepath)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
        
    for page in writer.pages:
        page.compress_content_streams()
        
    out_path = filepath + '.compressed.pdf'
    with open(out_path, 'wb') as f:
        writer.write(f)
        
    print(f"Compressed {filepath}: {os.path.getsize(out_path) / (1024*1024):.2f} MB")
    os.replace(out_path, filepath)

pdf_files = [
    "docs/0_General overview_dokumen kajian kerentanan dan risiko iklim_katingan.pdf",
    "docs/1_dokumen kajian desa karuing final layout.pdf",
    "docs/2_Kajian_Risiko_Bencana_Terkait_Iklim_Partisipatif_Desa_Tumbang_Habangoi.pdf",
    "docs/3_dok KRB IKLIM MANGARA KAWEI.pdf"
]

for f in pdf_files:
    if os.path.exists(f):
        compress_pypdf(f)
