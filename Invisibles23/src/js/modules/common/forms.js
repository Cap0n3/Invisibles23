import JustValidate from 'just-validate';
import emailjs, { send } from '@emailjs/browser';
import { displayMessage } from './utils/helpers';
import { getAPISecrets, sendEmail } from './utils/api';
import { renderRecaptchaV2, resetRecaptchaV2, createJustValidateRule } from './utils/helpers';

const nameRegex = /^[^#+±"*/()=?$£!%_;:,<>\d]+$/;
const addressRegex = /^[^#+±"*/()=?$£!%_;<>]+$/;
const messageRegex = /^[^\[\]{}<>]+$/;
const zipcodeRegex = /^[a-zA-Z0-9]{2,}\s?-?[a-zA-Z0-9]{0,}$/;
// The displayed date is formatted based on the locale of the user's browser, 
// but the parsed value is always formatted yyyy-mm-dd.
const birthdateRegex = /^\d{4}-\d{1,2}-\d{1,2}$/;
const phoneRegex = /^(\+(41|33)|00\s?(41|33)|0\d{1,2})(\s?\(0\))?(\s)?(\d{1,2})(\s)?(\d{2,3})(\s)?(\d{2})(\s)?(\d{2})(\s)?(\d{2})?$/;

/**
 * Validate a website forms with JustValidate
 * 
 * @param {*} formID 
 */
export function formValidation(formID) {
    const form = document.querySelector(formID);
    
    const validator = new JustValidate(formID, {
        successFieldCssClass: 'is-valid', // CSS class to add when input is valid
        errorFieldCssClass: 'is-invalid', // CSS class to add when input is invalid
        errorLabelCssClass: 'invalid-feedback', // CSS class to add for error message
        validateBeforeSubmitting: false,
    });

    const inputs = form.querySelectorAll('input, textarea');

    inputs.forEach((input) => {
        const inputType = input.getAttribute('type');
        const inputID = input.getAttribute('id');
        const inputName = input.getAttribute('name');
        const isTextarea = (input.nodeName === 'TEXTAREA');
        const isRequired = input.hasAttribute('required');
        const rules = [];

        // Check input attributes and add required rule
        if(isRequired) {
            rules.push(createJustValidateRule("required"));
        }

        // Then add other rules based on input type
        if (inputType === 'text' || isTextarea) {
            rules.push(
                createJustValidateRule("minLength", inputName === 'address' ? 5 : 2),
                createJustValidateRule("maxLength", isTextarea ? 10000 : (inputName === 'address' ? 100 : 50)),
                inputName === 'zip_code' ? 
                createJustValidateRule("customRegexp", zipcodeRegex, "Le code postal entré n'est pas valide") :
                createJustValidateRule("customRegexp", isTextarea ? messageRegex : (inputName === 'address' ? addressRegex : nameRegex))
            );
        } else if (inputType === 'number') {
            rules.push(
                createJustValidateRule("minLength", 3),
                createJustValidateRule("maxLength", 20),
                createJustValidateRule("integer")
            );
            
        } else if (inputType === 'email') {
            rules.push(
                createJustValidateRule("email")
            );
        }
        else if (inputType === 'date') {
            rules.push(
                createJustValidateRule("customRegexp", birthdateRegex, "Veuillez entrer une date valide (JJ/MM/AAAA)")
            )
        }
        else if (inputType === 'tel') {
            rules.push(
                createJustValidateRule("minLength", 5),
                createJustValidateRule("maxLength", 80),
                createJustValidateRule("customRegexp", phoneRegex, "Le numéro de téléphone n'est pas valide (ex: +41 79 123 45 67, 0033 6 12 34 56 78, 079 123 45 67)")
            );
        }
        
        // Add field to validator if it's not a hidden or submit input
        if(inputType !== 'hidden' && inputType !== 'submit') {
            try {
                validator.addField(`#${inputID}`, rules);
            } catch (error) {
                console.error("Error adding field to validator, check the input ID");
                console.log(input)
                console.log(rules);
                console.log(error);
            }
        }        
    });

    validator.onSuccess((formEvent) => {

        if (formID === "#contactForm" || formID === "#contactFormPage") {
            // Get active recaptcha container
            const ID_attibute = formEvent.target.getAttribute("id");
            const recaptchaContainer = document.querySelector(`#recaptcha-container_${ID_attibute}`);
            
            // Render recaptcha
            renderRecaptchaV2(recaptchaContainer, "6LdTY1wnAAAAABgHJBw3x5grn3iQvtKvefKdSks2", handleSubmit, formEvent);
        } else {
            // Let submit event continue if it's a django form (here it's membmership form)
            form.submit()
        }
    });
}

async function handleSubmit(formObject, token) {
    const toggleSpinner = (showSpinner) => {
        if (showSpinner) {
            spinner.style.display = "inline-block";
            submitText.style.display = "none";
        } else {
            spinner.style.display = "none";
            submitText.style.display = "inline-block";
        }
    }

    // Get spinner class and submit text
    const spinner = document.querySelector(".submit-spinner");
    const submitText = document.querySelector(".submit-text");

    // Get form input values and put them in an object
    const formData = {
        first_name: formObject.target.elements["first_name"].value,
        last_name: formObject.target.elements["last_name"].value,
        email: formObject.target.elements["email"].value,
        message: formObject.target.elements["message"].value,
        recaptcha_token: token
    };

    // Send email
    try { 
        // Display spinner
        toggleSpinner(true);  
        // Send email
        await sendEmail(formData);
        // Display success message
        displayMessage(
            formObject, 
            "Votre message a bien été envoyé. Merci !", 
            {
                success: "#successMessage", 
                error: "#errorMessage"
            }, 
            "success"
        );
        resetRecaptchaV2(formObject);
    }
    catch(error) {
        // Display error message
        displayMessage(
            formObject, 
            "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site.", 
            {
                success: "#successMessage",
                error: "#errorMessage"
            },
            "error"
        );
        resetRecaptchaV2(formObject);
    } finally {
        // Hide spinner
        toggleSpinner(false);
    }
}
