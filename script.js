document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu handling
    const menuToggle = document.querySelector('.navbar-toggler');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const navMenu = document.querySelector('.navbar-collapse');
            navMenu.classList.toggle('show');
        });
    }

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Active link highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Lazy loading images
    document.querySelectorAll('img[data-src]').forEach(img => {
        img.setAttribute('src', img.getAttribute('data-src'));
        img.onload = function() {
            img.removeAttribute('data-src');
        };
    });
});
