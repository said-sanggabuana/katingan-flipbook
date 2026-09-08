# Deployment & Hub Page Plan

## What
Create a central hub page (`index.html`) to link to all 4 flipbooks, and deploy the entire project to a zero-cost static hosting provider (e.g., GitHub Pages or Render).

## Why
The user requested a single web interface for readers to select a report, and a zero-cost deployment to make the flipbooks publicly accessible.

## How
1. **Clarify Platform:** Determine the user's preferred free host (GitHub Pages, Render, etc.).
2. **Compress Large Files:** Two PDFs exceed the 100MB strict limit of free tiers (138MB and 101MB). We will write a Python script (using PyMuPDF) to compress these files down to web-friendly sizes (<100MB).
3. **Build Hub Page:** Create `index.html` with a Tailwind CSS grid layout matching the WWF green styling, linking to the 4 HTML flipbooks in `/docs`.
4. **Deploy:** Initialize Git, commit the files (excluding the >100MB originals), and push to the chosen platform.

## Risks
- **File Size Limits:** If compression ruins image quality, we may need to explore alternative hosting for the raw PDFs (like Cloudflare R2).
- **CORS Issues:** The flipbooks use local `.pdf` files. On a static host, this works perfectly as long as the relative paths are correct.

## Alternatives Considered
- **Object Storage Hosting:** We considered hosting the PDFs on an S3-compatible free tier (like Cloudflare R2) and fetching them via URL to bypass the 100MB Git limit without compressing them. However, compression is generally preferred for web viewing to ensure fast loading times for users on slower networks.
