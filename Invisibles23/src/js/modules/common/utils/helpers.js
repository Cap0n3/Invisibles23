const axios = require('axios');

/**
 * Function to expand text with a toggle link to show more or less text.
 * 
 * @param {*} textWrapperClass - The class of the wrapper of the text to expand
 * @param {*} limit - The number of words to show before the toggle link
 */
export function expandText(textWrapperClass, limit = 20) {
    const wrappers = document.querySelectorAll(`.${textWrapperClass}`);

    wrappers.forEach((wrapper, index) => {
        let isExpanded = false;
        const fullText = wrapper.innerText;

        // get paragraph of the wrapper with the text
        const paragraph = wrapper.querySelector('p');


        // Count number of words
        const wordCount = fullText.split(" ").length;

        // If the text is shorter than the limit, do nothing
        if (wordCount <= limit) {
            return;
        }
        
        // Extract the first 20 words and add "..." at the end
        const words = fullText.split(" ");
        let excerpt = words.slice(0, limit).join(" ");
        excerpt += " ...";
        paragraph.innerText = excerpt;

        // Create the toggle link
        const toggleLink = document.createElement("a");
        toggleLink.setAttribute("class", "ressource-toggle");
        toggleLink.innerText = "Voir plus";
        
        // Add the toggle link after the text
        paragraph.appendChild(toggleLink);

        // Add event listener to the toggle link
        toggleLink.addEventListener("click", toggleText);

        // Function to toggle the visibility of the full text
        function toggleText() {
            if (isExpanded) {
                // Show the excerpt
                paragraph.innerText = excerpt;
                paragraph.appendChild(toggleLink);
                toggleLink.innerText = "Voir plus";
            } else {
                // add text to the paragraph
                paragraph.innerText = fullText;
                // Show the full text
                //wrapper.innerText = fullText;
                paragraph.appendChild(toggleLink);
                toggleLink.innerText = "Voir moins";
            }
            isExpanded = !isExpanded;
        }
    })
}

/**
 * Function to display a message on the form. 
 * It will display a success message if the form was submitted successfully, or an error message if there was an error.
 * 
 * @param {Object} formObject - The form object
 * @param {String} statusMessage - The message to display
 * @param {Object} containersID - The IDs of the containers for the success, warning and error messages
 * @param {String} type - The type of message (success or error)
 * @returns {void}
 * 
 * @example
 * displayMessage(
 *  formObject,
 *  "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site.",
 *  {
 *      success: "#successMessage",
 *      warning: "#warningMessage",
 *      error: "#errorMessage",
 *  },
 *  "error"
 * );
 * 
 * @example
 * displayMessage(
 *  formObject,
 *  "Votre adresse email a bien été ajoutée à la liste de diffusion. Merci !",
 *  {
 *      success: "#successMessage",
 *      warning: "#warningMessage",
 *      error: "#errorMessage",
 *  },
 *  "success"
 * );
 */
export function displayMessage(formObject, statusMessage, containersID, type) {
    const currentForm = formObject.target;
    // Get containers for success and error messages
    const successContainer = currentForm.querySelector(containersID.success);
    const warningContainer = currentForm.querySelector(containersID.warning);
    const errorContainer = currentForm.querySelector(containersID.error);
    const inputs = Array.from(currentForm.querySelectorAll("input, textarea"));

    const showMessage = (container, message) => {
        container.innerHTML = message;
        container.classList.replace("hideMessage", "showMessage");
    };

    const hideMessage = (container) => {
        container.classList.replace("showMessage", "hideMessage");
    };

    const resetForm = () => {
        inputs.forEach((input) => input.classList.remove("is-valid"));
        currentForm.reset();
    };

    if (type === "success") {
        showMessage(successContainer, statusMessage);
        setTimeout(() => {
            hideMessage(successContainer);
            resetForm();
        }, 3000);
    }
    else if (type === "warning") {
        showMessage(warningContainer, statusMessage);
        setTimeout(() => {
            hideMessage(warningContainer);
            resetForm();
        }, 5000);
    }
    else if (type === "error") {
        showMessage(errorContainer, statusMessage);
        setTimeout(() => {
            hideMessage(errorContainer);
            resetForm();
        }, 5000);
    }
}

export function getCookie(name) {
    const cookies = document.cookie.split(';');
    const rawCookie = cookies.find(cookie => cookie.startsWith(name));
    return rawCookie.split('=')[1];
}

/**
 * Make sure recapcha is loaded before rendering it (seems ok without but just in case ...).
 */
export function initRecaptchaV2() {
    
    if(typeof grecaptcha === 'undefined') {
        grecaptcha = {};
      }
      grecaptcha.ready = function(cb){
        if(typeof grecaptcha === 'undefined') {
          // window.__grecaptcha_cfg is a global variable that stores reCAPTCHA's
          // configuration. By default, any functions listed in its 'fns' property
          // are automatically executed when reCAPTCHA loads.
          const c = '___grecaptcha_cfg';
          window[c] = window[c] || {};
          (window[c]['fns'] = window[c]['fns']||[]).push(cb);
        } else {
          cb();
        }
      }
}

/**
 * Render recaptcha v2 in the given container and match captcha box design for small screens.
 * 
 * @param {String} container - The ID of the container where to render recaptcha
 * @param {String} sitekey - The sitekey of the recaptcha
 * @param {Function} submit - The function to execute when the recaptcha is validated
 * @param {Object} formEvent - The event object of the form
 */
export function renderRecaptchaV2 (container, sitekey, submit, formEvent) {
    // Check if recaptcha is already rendered to avoid error
    const isRecaptchaRendered = container.hasAttribute("data-widget-rendered");

    // Make recaptcha appear if captcha was already loaded
    if (container.style.display === "none") {
        container.style.display = "block";
    }

    // check if screen width is between 1090 and 992 or smaller than 451 (for form responsive design purpose)
    const isSmallScreen = window.matchMedia("only screen and (max-width: 1090px) and (min-width: 992px)").matches || window.matchMedia("only screen and (max-width: 451px)").matches;

    // Avoid multiple rendering of recaptcha
    if(!isRecaptchaRendered) {
        // Set attribute to avoid multiple rendering of recaptcha
        container.setAttribute("data-widget-rendered", "true");
        // Render recaptcha
        grecaptcha.ready(function () {
            grecaptcha.ready(function() {
                grecaptcha.render(container, {
                    sitekey: sitekey,
                    callback: function(token) {
                        //get id of the form
                        submit(formEvent, token);   
                    },
                    size: isSmallScreen ? "compact" : "normal",
                });
            });                      
        });
    }
}

/**
 * Reset recaptcha v2 and hide it.
 * 
 * @param {Object} formObject - The form object to get the form id
 */
export function resetRecaptchaV2(formObject) {
    // Get form id to get to the right recaptcha container
    const ID_attibute = formObject.target.getAttribute("id");
    // get recaptcha container
    const container = document.querySelector(`#recaptcha-container_${ID_attibute}`);

    // Reset recaptcha
    grecaptcha.reset(container);
    container.style.display = "none";
}


/**
 * Helper function to create just-validate rules and make code drier.
 * 
 * @param {String} rule - The rule to create (required, minLength, maxLength, customRegexp, integer, email)
 * @param {String} value - The parameter of the rule for minLength, maxLength or customRegexp (optional)
 * @param {String} customMessage - The custom message to display if the rule is not respected (optional)
 *
 * @returns {Object} - The rule object to pass to just-validate
 */ 
export function createJustValidateRule(rule, value="", customMessage="") {
    switch(rule) {
        case "required":
            return { rule: 'required', errorMessage: customMessage || "Ce champ est obligatoire" }
            break;
        case "minLength":
            return { rule: 'minLength', value: value, errorMessage: customMessage || `Ce champ doit contenir au minimum ${value} caractères` }
            break;
        case "maxLength":
            return { rule: 'maxLength', value: value, errorMessage: customMessage || `Ce champ doit contenir au maximum ${value} caractères` }
            break;
        case "customRegexp":
            return { rule: 'customRegexp', value: value, errorMessage: customMessage || "Un caractère non autorisé a été entré" }
            break;
        case "integer":
            return { rule: 'integer', errorMessage: customMessage || "Ce champ doit contenir un nombre entier" }
            break;
        case "email":
            return { rule: 'email', errorMessage: customMessage || "Veuillez entrer une adresse email valide" }
            break;
        default:
            console.error("Error: no rule found");
    }
}