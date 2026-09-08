document.addEventListener('DOMContentLoaded', function() {
    const rawContent = document.getElementById('raw-content');
    const flipbookEl = document.getElementById('flipbook');
    const tocList = document.getElementById('toc-list');
    
    // Page dimensions
    const PAGE_WIDTH = 450;
    const PAGE_HEIGHT = 600;
    
    // Measuring container (off-screen but rendered)
    const measureContainer = document.createElement('div');
    measureContainer.style.position = 'absolute';
    measureContainer.style.top = '-9999px';
    measureContainer.style.left = '-9999px';
    measureContainer.style.width = PAGE_WIDTH + 'px';
    measureContainer.style.height = PAGE_HEIGHT + 'px';
    measureContainer.style.visibility = 'hidden';
    document.body.appendChild(measureContainer);

    let pageCount = 0;
    
    // Front Cover
    createCover('KATINGAN', 'CLIMATE RISK ASSESSMENT');
    
    const chapters = Array.from(rawContent.querySelectorAll('.chapter-divider, .chapter-content'));
    
    chapters.forEach(chapterBlock => {
        if (chapterBlock.classList.contains('chapter-divider')) {
            const title = chapterBlock.querySelector('h1').innerText;
            createDivider(title);
        } else if (chapterBlock.classList.contains('chapter-content')) {
            let currentMeasurePage = createMeasurePage();
            let actualPage = createPage();
            
            const elements = Array.from(chapterBlock.childNodes);
            
            elements.forEach(el => {
                if (el.nodeType === Node.ELEMENT_NODE) {
                    currentMeasurePage.appendChild(el.cloneNode(true));
                    
                    // Allow a little padding buffer for height
                    if (currentMeasurePage.scrollHeight > PAGE_HEIGHT - 60) {
                        // Overflow! Start a new page
                        currentMeasurePage = createMeasurePage();
                        currentMeasurePage.appendChild(el.cloneNode(true)); // Add to new page
                        
                        actualPage = createPage();
                        actualPage.querySelector('.page-content').appendChild(el);
                    } else {
                        actualPage.querySelector('.page-content').appendChild(el);
                    }
                }
            });
            // Ensure even pages for spreads
            if (pageCount % 2 !== 0) {
                createPage();
            }
        }
    });

    // Back Cover
    createCover('', 'WWF Indonesia 2026');

    // Remove raw content and measure container
    rawContent.remove();
    measureContainer.remove();

    // Initialize StPageFlip
    const pageFlip = new St.PageFlip(document.getElementById('flipbook'), {
        width: PAGE_WIDTH,
        height: PAGE_HEIGHT,
        size: "fixed",
        minWidth: 300,
        maxWidth: 600,
        minHeight: 400,
        maxHeight: 800,
        maxShadowOpacity: 0.5,
        showCover: true,
        mobileScrollSupport: false
    });

    pageFlip.loadFromHTML(document.querySelectorAll('.page'));

    // Setup TOC Links
    document.querySelectorAll('#toc-list a').forEach(a => {
        a.addEventListener('click', (e) => {
            e.preventDefault();
            const pageNum = parseInt(a.getAttribute('data-page'));
            pageFlip.turnToPage(pageNum);
        });
    });

    function createMeasurePage() {
        measureContainer.innerHTML = '';
        const content = document.createElement('div');
        content.classList.add('page-content');
        measureContainer.appendChild(content);
        return content;
    }

    function createPage() {
        const page = document.createElement('div');
        page.classList.add('page');
        const content = document.createElement('div');
        content.classList.add('page-content');
        page.appendChild(content);
        flipbookEl.appendChild(page);
        pageCount++;
        return page;
    }

    function createDivider(title) {
        // Ensure dividers fall on the right side (odd page number considering cover is 0)
        if (pageCount % 2 !== 0) {
            createPage(); // blank page to force right side
        }
        
        const page = document.createElement('div');
        page.classList.add('page', '--hard');
        
        const divider = document.createElement('div');
        divider.classList.add('page-divider');
        divider.innerHTML = `<h1>${title}</h1>`;
        page.appendChild(divider);
        
        flipbookEl.appendChild(page);
        
        // Add to TOC
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.innerText = title;
        a.setAttribute('data-page', pageCount);
        li.appendChild(a);
        tocList.appendChild(li);
        
        pageCount++;
    }

    function createCover(title, subtitle) {
        const page = document.createElement('div');
        page.classList.add('page', 'page-cover', '--hard');
        page.innerHTML = `
            <div class="page-content" style="column-count: 1; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center;">
                <h1 style="font-size: 3rem; color: var(--accent); margin-bottom: 1rem;">${title}</h1>
                <h2 style="font-size: 1.5rem; color: var(--secondary);">${subtitle}</h2>
            </div>
        `;
        flipbookEl.appendChild(page);
        pageCount++;
    }
});
