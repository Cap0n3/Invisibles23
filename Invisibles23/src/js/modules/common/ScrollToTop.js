export function scrollToTop() {
    const scrollToTopButton = document.getElementById('scrollToTopButton');

    window.addEventListener("scroll", event => {
        const scrollPos = document.documentElement.scrollTop
        if (scrollPos > 300) {
            scrollToTopButton.style.display = 'block';
        } else {
            scrollToTopButton.style.display = 'none';
        }
    }, {passive: true})

    scrollToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}