document.addEventListener('DOMContentLoaded', function () {
    // Initialize highlighting immediately
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }

    const lightTheme = document.getElementById('light-theme');
    const darkTheme = document.getElementById('dark-theme');
    const themeToggle = document.getElementById('themeToggle');

    function setTheme(isDark) {
        document.documentElement.classList.toggle('dark', isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');

        if (lightTheme) lightTheme.disabled = isDark;
        if (darkTheme) darkTheme.disabled = !isDark;
    }

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme === 'dark');
    } else {
        setTheme(window.matchMedia('(prefers-color-scheme: dark)').matches);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            setTheme(!document.documentElement.classList.contains('dark'));
        });
    }

    // Initialize search if elements exist
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        loadSearchIndex();

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value;
            const resultsDiv = document.getElementById('searchResults');

            if (query.length < 2) {
                resultsDiv.style.display = 'none';
                return;
            }

            if (!idx) return;

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
            const resultsDiv = document.getElementById('searchResults');
            if (resultsDiv && !e.target.closest('.search-container')) {
                resultsDiv.style.display = 'none';
            }
        });
    }
});

let searchIndex = null;
let idx = null;

// Load search index
async function loadSearchIndex() {
    try {
        const response = await fetch('/search-index.json');
        searchIndex = await response.json();

        // Build lunr index
        if (typeof lunr !== 'undefined') {
            idx = lunr(function () {
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
    } catch (e) {
        console.error("Failed to load search index:", e);
    }
}
