# [Tech Spec] Katingan Climate Report Interactive Flipbooks

**Author:** Antigravity (AI Agent)
**Status:** Draft
**Date:** 2026-09-08

---

### 1. Overview & Goals
* **Summary:** Create 4 interactive HTML flipbooks corresponding to the 4 PDF climate reports in the `docs` directory. The flipbooks will dynamically render the PDFs in-browser to preserve text quality.
* **Goals:** 
  - Render PDFs using PDF.js.
  - Implement realistic page flipping using StPageFlip.
  - Provide standard controls: Next/Prev, Page Slider, Zoom, Download.
  - Apply a WWF/Climate professional theme (light background, green accents).
* **Non-Goals:** Complex backend integration, static image generation server-side, advanced search/TOC extraction.

### 2. Architecture & System Flow

```
[ Web Browser ]  --->  [ Standalone HTML File ]
                              |
                              v (Loads via CDN)
                        [ PDF.js ] -> Parses local PDF file
                        [ StPageFlip ] -> Manages 3D flip effects & canvas
```

* **Components:** 
  - HTML UI Shell (TailwindCSS for WWF theme).
  - JavaScript Controller (PDF.js loader, Canvas renderer, StPageFlip initialization).
  - 4 HTML files mapping to the 4 PDFs.

### 3. Detailed Specification

#### A. File Structure Output
* `docs/kajian_kerentanan_dan_risiko_iklim_katingan.html`
* `docs/kajian_kerentanan_dan_risiko_iklim_desa_karuing.html`
* `docs/Kajian_Kerentanan_dan_Risiko_Iklim_Desa_Tumbang_Habangoi.html`
* `docs/Kajian_Kerentanan_dan_Risiko_Iklim_Desa_Tumbang_Mangara_dan_Kawei.html`

#### B. Technical Implementation (JS)
* Use `pdfjs-dist` to load the target PDF.
* On load, fetch `numPages` and initialize the StPageFlip container.
* Since StPageFlip works well with HTML elements, we will use a hybrid approach: Create div wrappers for pages and use PDF.js to render the page onto a `<canvas>` element inside each div as they are flipped (or lazy-loaded).

### 4. Trade-Offs & Alternatives Considered
| Approach | Pros | Cons | Decision |
| :--- | :--- | :--- | :--- |
| **PDF.js + StPageFlip (Selected)** | High text quality, no bloated image folders | Higher client-side memory usage | Selected |
| **Pre-rendered Images** | Fast initial load for single pages | Huge storage cost for large PDFs | Rejected |

### 5. Operational Considerations
* **Hosting:** The files are designed to be deployed to a static web server.
* **Local Testing:** Must be viewed through a local web server (e.g., Python `http.server`) due to CORS restrictions when PDF.js fetches local files.
