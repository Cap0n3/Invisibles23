
/**
 * Scroll down to the search results in ressources pages
 */
export function searchBehavior() {
    const fullUrl = window.location.href;
    const isKeywords = fullUrl.match(/keywords=([^&]*)/)
    if(isKeywords) {
        if(isKeywords[1] !== '') {
            // Scroll down to the search results
            window.scrollTo({
                top: 400,
                behavior: 'smooth'
            });
        }
    }
}