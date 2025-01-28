document.addEventListener('DOMContentLoaded', function() {
    hljs.highlightAll();
    
    const lightTheme = document.getElementById('light-theme');
    const darkTheme = document.getElementById('dark-theme');
    
    function loadTheme(themeName) {
        const themeLink = document.createElement('link');
        themeLink.rel = 'stylesheet';
        themeLink.href = `https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/${themeName}.min.css`;
        document.head.appendChild(themeLink);
        return themeLink;
    }
    
    function setTheme(isDark) {
        document.body.classList.toggle('dark-theme', isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        
        lightTheme.disabled = isDark;
        darkTheme.disabled = !isDark;
        
        document.querySelectorAll('pre code[theme]').forEach(block => {
            const customTheme = block.getAttribute('theme');
            if (customTheme) {
                // Load theme if not already loaded
                if (!document.querySelector(`link[href*="${customTheme}.min.css"]`)) {
                    loadTheme(customTheme);
                }
                
                block.className = block.className.replace(/\b\w+\b/g, '');
                block.classList.add('language-' + block.getAttribute('lang'));
                block.classList.add(isDark ? customTheme : 'github');
                hljs.highlightElement(block);
            }
        });
    }
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme === 'dark');
    } else {
        setTheme(window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
    
    document.getElementById('themeToggle').addEventListener('click', () => {
        setTheme(!document.body.classList.contains('dark-theme'));
    });
});


let searchIndex = null;
let idx = null;

// Load search index
async function loadSearchIndex() {
    const response = await fetch('/search-index.json');
    searchIndex = await response.json();
    
    // Build lunr index
    idx = lunr(function() {
        this.field('title', { boost: 10 });
        this.field('description', { boost: 5 });
        this.field('content');
        this.field('tags', { boost: 5 });
        
        searchIndex.forEach((doc, i) => {
            doc.id = i;
            this.add(doc);
        });
    });
}

// Search handler
document.getElementById('searchInput').addEventListener('input', (e) => {
    const query = e.target.value;
    const resultsDiv = document.getElementById('searchResults');
    
    if (query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
    }
    
    const results = idx.search(query);
    if (results.length) {
        resultsDiv.innerHTML = results
            .slice(0, 5)
            .map(r => searchIndex[r.ref])
            .map(doc => `
                <div class="search-result-item" onclick="window.location='${doc.url}'">
                    <div class="title">${doc.title}</div>
                    <div class="description">${doc.description}</div>
                </div>
            `).join('');
        resultsDiv.style.display = 'block';
    } else {
        resultsDiv.innerHTML = '<div class="search-result-item">No results found</div>';
        resultsDiv.style.display = 'block';
    }
});

// Close search results when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        document.getElementById('searchResults').style.display = 'none';
    }
});

// Initialize search
loadSearchIndex();
