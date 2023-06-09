import { navbar } from "./modules/common/navbar.js";
import { contactForm } from "./modules/common/contactForm.js";
import { homepagePodcasts, podcastsPage } from "./modules/insertPodcasts.js";

/**
 * Initialize the webpage
 */
function initialize() {
    
    const currentPage = window.location.pathname;
    
    navbar(); // Initialize the navbar
    
    if (currentPage === '/') {
        contactForm(); // Initialize the contact form
        homepagePodcasts(); // Get and create the last podcasts for the homepage section
    }
    else if (currentPage === '/podcasts/') {
        podcastsPage(); // Get and create all the podcasts for podcasts page
    }
    

    // Initialize bootstrap popovers (to remove if not used)
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}

window.onload = initialize;