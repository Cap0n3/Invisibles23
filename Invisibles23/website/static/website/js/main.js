import { navbar } from "./modules/common/navbar.js";
import { getLastPodcasts } from "./modules/common/utils/api.js";

function initialize() {
    // Call functions to initialize the webpage
    navbar();
    getLastPodcasts();
}

window.onload = initialize;