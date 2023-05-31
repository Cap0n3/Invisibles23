export function navbar() {
    /**
     * Make navbar appear/disappear when scrolling.
     */
    window.addEventListener("scroll", event => {
        const scrollPos = document.documentElement.scrollTop
        const nav = document.getElementsByClassName("navbar")
        
        if(scrollPos >= 70) {
            nav.item(0).classList.add("show")
        }
        else {
            nav.item(0).classList.remove("show")
        }  
    }, {passive: true})
}
