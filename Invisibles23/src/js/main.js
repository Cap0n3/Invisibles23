import { navbar } from "./modules/common/navbar.js";
import { getLastPodcasts } from "./modules/common/utils/api.js";
import { contactForm } from "./modules/common/contactForm.js";
import { createPodcasts } from "./modules/createPodcasts.js";

function initialize() {
    // Call functions to initialize the webpage
    navbar();
    //getLastPodcasts();
    contactForm();

    // For testing purposes
    createPodcasts();
}

window.onload = initialize;