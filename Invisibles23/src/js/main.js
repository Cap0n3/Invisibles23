import { navbar } from "./modules/common/navbar.js";
import { getLastPodcasts } from "./modules/common/utils/api.js";
import { contactForm } from "./modules/common/contactForm.js";
import { homepagePodcasts } from "./modules/homepagePodcasts.js";
import { podcastsPage } from "./modules/podcastsPage.js";

function initialize() {
    // Call functions to initialize the webpage
    
    navbar();
    contactForm();
    homepagePodcasts(); // Get and create the last podcasts for the homepage section
    podcastsPage(); // Get and create all the podcasts for podcasts page

    // Initialize bootstrap popovers (to remove if not used)
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}

window.onload = initialize;