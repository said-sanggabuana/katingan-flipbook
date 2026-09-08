import os

output_dir = 'flipbook_project'
html_path = os.path.join(output_dir, 'index.html')
extracted_path = os.path.join(output_dir, 'extracted_content.html')

with open(extracted_path, 'r', encoding='utf-8') as f:
    extracted = f.read()

template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Climate Risk Assessment Flipbook</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="toc">
            <h3>Table of Contents</h3>
            <ul id="toc-list">
            </ul>
        </div>
        
        <div class="flipbook-wrapper">
            <div id="flipbook" class="flipbook">
            </div>
        </div>
    </div>

    <div id="raw-content" style="display: none;">
        {extracted}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
    <script src="js/main.js"></script>
</body>
</html>"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(template)
