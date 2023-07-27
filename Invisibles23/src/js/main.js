import { navbar } from "./modules/common/navbar.js";
import { scrollToTop } from "./modules/common/ScrollToTop.js";
import { formValidation } from "./modules/common/forms.js";
import { homepagePodcasts, podcastsPage } from "./modules/insertPodcasts.js";
import { searchBehavior } from "./modules/ressources.js";
import { expandText } from "./modules/common/utils/helpers.js";
import { newsletterForm } from "./modules/common/newsletterForm.js";
import { initRecaptchaV2 } from "./modules/common/utils/helpers.js";

/**
 * Initialize the webpage
 */
async function initialize() {    
    const currentPage = window.location.pathname;

    navbar(); // Initialize the navbar
    scrollToTop(); // Initialize the scroll to top button
    newsletterForm("newsletterFooter"); // Initialize the newsletter form (footer)

    initRecaptchaV2(); // Initialize the recaptcha v2
   
    if (currentPage === '/') {
        formValidation("#contactForm"); // Initialize the contact form
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
        formValidation("#contactFormPage"); // Initialize the contact form
    }
    else if (currentPage === '/membership/') {
        formValidation("#membershipForm"); // Initialize the membership form
    }
    
    // Initialize bootstrap popovers (to remove if not used)
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}

window.onload = initialize;