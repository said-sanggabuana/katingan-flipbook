import fitz
import os
import re

docs_dir = 'docs'
output_dir = 'flipbook_project'
assets_dir = os.path.join(output_dir, 'assets', 'images')
js_dir = os.path.join(output_dir, 'js')
css_dir = os.path.join(output_dir, 'css')

os.makedirs(assets_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)
os.makedirs(css_dir, exist_ok=True)

pdf_files = [
    '0_General overview_dokumen kajian kerentanan dan risiko iklim_katingan.pdf',
    '1_dokumen kajian desa karuing final layout.pdf',
    '2_Kajian_Risiko_Bencana_Terkait_Iklim_Partisipatif_Desa_Tumbang_Habangoi.pdf',
    '3_dok KRB IKLIM MANGARA KAWEI.pdf'
]

# A dictionary to hold the structured content
structured_content = {}

def clean_text(text):
    # Remove excessive newlines
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

for pdf_file in pdf_files:
    pdf_path = os.path.join(docs_dir, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"Skipping {pdf_file}, not found.")
        continue
        
    print(f"Processing {pdf_file}...")
    doc = fitz.open(pdf_path)
    
    chapter_title = pdf_file.split('_')[1].replace('.pdf', '').title()
    structured_content[chapter_title] = []
    
    image_counter = 0
    
    # Extract only the first 15 pages of each document to keep it concise, 
    # focusing on executive summaries and key findings, as well as preserving context.
    num_pages = min(15, len(doc)) 
    
    for page_num in range(num_pages):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        page_text = ""
        for b in blocks:
            if b['type'] == 0:  # Text block
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        size = s["size"]
                        if len(text) > 3:
                            # Heuristic: Larger font sizes are headers/callouts
                            if size > 14:
                                page_text += f"\n<h2 class='callout'>{clean_text(text)}</h2>\n"
                            elif size > 11:
                                page_text += f"\n<h3>{clean_text(text)}</h3>\n"
                            else:
                                page_text += f"{clean_text(text)} "
            
            elif b['type'] == 1:  # Image block
                image_counter += 1
                # Filter small icons/logos
                if b["width"] > 200 and b["height"] > 200:
                    try:
                        base_image = doc.extract_image(b["number"])
                        if base_image:
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            image_filename = f"{chapter_title.replace(' ', '_')}_{page_num}_{image_counter}.{image_ext}"
                            image_filepath = os.path.join(assets_dir, image_filename)
                            with open(image_filepath, "wb") as img_file:
                                img_file.write(image_bytes)
                            page_text += f'\n<img src="assets/images/{image_filename}" class="pdf-image" alt="Extracted Chart/Map">\n'
                    except Exception as e:
                        print(f"Failed to extract image: {e}")
        
        # Clean up paragraphs
        paragraphs = page_text.split('\n')
        cleaned_paragraphs = []
        for p in paragraphs:
            p = p.strip()
            if not p: continue
            if p.startswith('<h') or p.startswith('<img'):
                cleaned_paragraphs.append(p)
            else:
                if len(p) > 20: # skip page numbers or tiny text
                    cleaned_paragraphs.append(f'<p>{p}</p>')
                
        if cleaned_paragraphs:
            structured_content[chapter_title].append('\n'.join(cleaned_paragraphs))

html_content = ""
for chapter, pages in structured_content.items():
    html_content += f'<div class="chapter-divider" id="{chapter.replace(" ", "-")}">\n'
    html_content += f'  <h1>{chapter}</h1>\n'
    html_content += f'</div>\n'
    
    html_content += f'<div class="chapter-content">\n'
    for page in pages:
        html_content += page + "\n"
    html_content += f'</div>\n'

with open(os.path.join(output_dir, 'extracted_content.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Extraction complete.")
