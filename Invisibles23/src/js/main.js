import { navbar } from "./modules/common/navbar.js";
import { contactForm } from "./modules/common/contactForm.js";
import { homepagePodcasts, podcastsPage } from "./modules/insertPodcasts.js";
import { searchBehavior } from "./modules/ressources.js";
import { expandText } from "./modules/common/utils/helpers.js";
import { newsletterForm } from "./modules/common/newsletterForm.js";

/**
 * Initialize the webpage
 */
function initialize() {    
    const currentPage = window.location.pathname;
    
    navbar(); // Initialize the navbar
    newsletterForm("newsletterFooter"); // Initialize the newsletter form (footer)
   
    if (currentPage === '/') {
        console.log("home_")
        contactForm("#contactForm"); // Initialize the contact form
        homepagePodcasts(); // Get and create the last podcasts for the homepage section
        newsletterForm("newsletterC2A"); // Initialize the newsletter form (c2a section)
    }
    else if (currentPage === '/podcasts/') {
        podcastsPage(); // Get and create all the podcasts for podcasts page
    }
    else if (/ressources/.test(currentPage)) {
        searchBehavior(); // Initialize search behavior
        expandText('card-text', 25); // Initialize the expand text behavior
    }
    else if (currentPage === '/contact/') {
        contactForm("#contactFormPage"); // Initialize the contact form
    }
    
    // Initialize bootstrap popovers (to remove if not used)
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}

window.onload = initialize;