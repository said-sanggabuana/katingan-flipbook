import os
import io
import fitz
from PIL import Image

def compress_pymupdf(filepath):
    print(f"Original {filepath}: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
    out_path = filepath + '.compressed.pdf'
    
    doc = fitz.open(filepath)
    processed_xrefs = set()
    
    # Image downsampling settings
    max_dim = 1500
    quality = 65
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        for img in page.get_images():
            xref = img[0]
            if xref in processed_xrefs:
                continue
            processed_xrefs.add(xref)
            
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                im = Image.open(io.BytesIO(image_bytes))
                
                # Resize if larger than max_dim
                if im.width > max_dim or im.height > max_dim:
                    ratio = min(max_dim / im.width, max_dim / im.height)
                    new_size = (int(im.width * ratio), int(im.height * ratio))
                    im = im.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert color space for JPEG format
                if im.mode in ('RGBA', 'LA', 'P', 'CMYK'):
                    im = im.convert('RGB')
                    
                # Re-compress as optimized JPEG
                img_byte_arr = io.BytesIO()
                im.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                new_bytes = img_byte_arr.getvalue()
                
                # Only replace if the new image is smaller
                if len(new_bytes) < len(image_bytes):
                    page.replace_image(xref, stream=new_bytes)
            except Exception as e:
                # Silently skip images that cannot be processed (e.g. invalid formats)
                pass
                
    # garbage=4: removes unused objects, duplicate objects, and compacts xref table
    # deflate=True: compresses uncompressed streams (text, vectors)
    doc.save(out_path, garbage=4, deflate=True)
    doc.close()
    
    print(f"Compressed {filepath}: {os.path.getsize(out_path) / (1024*1024):.2f} MB\n")
    
    # Replace original with compressed
    os.replace(out_path, filepath)

pdf_files = [
    "docs/0_General overview_dokumen kajian kerentanan dan risiko iklim_katingan.pdf",
    "docs/1_dokumen kajian desa karuing final layout.pdf",
    "docs/2_Kajian_Risiko_Bencana_Terkait_Iklim_Partisipatif_Desa_Tumbang_Habangoi.pdf",
    "docs/3_dok KRB IKLIM MANGARA KAWEI.pdf"
]

for f in pdf_files:
    if os.path.exists(f):
        compress_pymupdf(f)
