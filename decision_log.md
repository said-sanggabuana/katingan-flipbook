# Decision Log - Katingan Climate Report Flipbooks

## Date: 2026-09-08
**Decision:** Implementation approach for converting 4 climate report PDFs into interactive HTML flipbooks.
**Context:** We need to present 4 Katingan climate report PDF files as interactive flipbooks for user-friendly reading.
**Decisions Made:**
1. **Tech Stack:** Use PDF.js with a modern flip library (like StPageFlip) to dynamically render PDF pages in the browser. This preserves text quality and prevents the bloat of static image extraction.
2. **Output Location:** 4 standalone HTML files will be created inside the `docs` directory alongside the original PDFs.
3. **UI/Theme:** Professional WWF / Climate Report theme (Clean light background, green/earth accents, corporate typography).
4. **Interactive Features:** Standard controls (Next/Prev buttons, Page Slider, Zoom, Download original PDF).
5. **Distribution:** The flipbooks are designed to be hosted on a web server as part of a larger project website, hence external dependencies will be loaded via CDN.

## Decision 6: Deployment & File Compression
**Date:** 2026-09-08
**Decision:** Use GitHub Pages for zero-cost deployment, compress PDFs using pypdf to bypass the 100MB Git limit, move HTML files to project root, and build a Tailwind grid index.html hub page.
**Rationale:** User requested a single hub page with zero cost hosting and a styled grid. GitHub Pages enforces a 100MB limit, so PDF compression was mandatory.


## Decision 7: PDF Path Fix for Deployment
**Date:** 2026-09-12
**Decision:** Prepend 'docs/' to PDF paths in the flipbook HTML files.
**Rationale:** The HTML files were moved to the project root, but the paths were still relative to the root, causing a 404 error when accessing the PDFs located in the 'docs' folder on GitHub Pages.
