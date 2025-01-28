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
