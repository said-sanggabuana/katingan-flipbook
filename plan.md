# Plan: Fix PDF Loading Path and Deploy

## What
Fix the broken PDF path in the HTML files and commit the changes to GitHub so the GitHub Pages deployment works correctly.

## Why
When the HTML files were moved to the root directory for GitHub Pages, the `build_flipbooks.py` template was not updated. It was still telling `pdf.js` to look for the PDFs in the root directory (e.g. `0_General overview...pdf`) instead of inside the `docs/` folder (e.g. `docs/0_General overview...pdf`). This caused a 404 Not Found error, making the page stuck on "Loading Report...".

## How
1. **Locally update `build_flipbooks.py`**: Change `pdfUrl` and the `<a download>` link to point to `docs/{{PDF_FILENAME}}`. (I have already tested this change locally and regenerated the HTML files).
2. **Commit the changes**: Stage the modified `build_flipbooks.py` and the 4 generated HTML files.
3. **Push to GitHub**: Push the commit to the `main` branch to trigger the GitHub Pages rebuild.

## Risks
- GitHub Pages might take a few minutes to invalidate its cache, so the fix might not appear instantly after pushing.
- Filenames have spaces, which standard web servers handle fine, but if GitHub Pages has a strict URL encoding issue, we might need to URL-encode the paths (though usually this is handled automatically by `pdf.js` and modern browsers).

## Alternatives Considered
- Moving the PDFs out of the `docs/` folder and into the root directory. However, keeping them in `docs/` is cleaner for project organization.
