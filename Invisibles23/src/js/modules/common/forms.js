import JustValidate from 'just-validate';
import emailjs, { send } from '@emailjs/browser';
import { displayMessage } from './utils/helpers';
import { getAPISecrets, sendEmail } from './utils/api';
import { renderRecaptchaV2, resetRecaptchaV2 } from './utils/helpers';

const nameRegex = /^[^#+±"*/()=?$£!%_;:<>]+$/;
const messageRegex = /^[^\[\]{}<>]+$/;

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
        const isTextarea = (input.nodeName === 'TEXTAREA');
        const rules = [];

        if (inputType === 'text' || isTextarea) {
            rules.push(
                {
                    rule: 'required',
                    errorMessage: "Ce champ est obligatoire",
                },
                {
                    rule: 'minLength',
                    value: 2,
                    errorMessage: "Ce champ doit contenir au moins 2 caractères",
                },
                {
                    rule: 'maxLength',
                    value: isTextarea ? 10000 : 50,
                    errorMessage: `Ce champ ne peut pas contenir plus de ${isTextarea ? 10000 : 50} caractères`,
                },
                {
                    rule: 'customRegexp',
                    value: isTextarea ? messageRegex : nameRegex,
                    errorMessage: "Un caractère invalide a été détecté",
                }
            );
        } else if (inputType === 'number') {
            rules.push(
                {
                    rule: 'required',
                    errorMessage: "Ce champ est obligatoire",
                },
                {
                    rule: 'minLength',
                    value: 3,
                    errorMessage: "Ce champ doit contenir au moins 3 chiffres",
                },
                {
                    rule: 'maxLength',
                    value: 20,
                    errorMessage: "Ce champ ne peut pas contenir plus de 20 chiffres",
                },
                {
                    rule: 'integer',
                    errorMessage: "Ce champ doit contenir un nombre entier",
                }
            );
            
        } else if (inputType === 'email') {
            rules.push(
                {
                    rule: 'required',
                    errorMessage: "Ce champ est obligatoire",
                },
                {
                    rule: 'email',
                    errorMessage: "Veuillez saisir une adresse email valide",
                }
            );
        } else if (inputType === 'radio') {
            rules.push(
                {
                    rule: 'required',
                    errorMessage: "Veuillez sélectionner une option",
                }
            );
        } else if (inputType === 'date') {
            rules.push(
                {
                    rule: 'required',
                    errorMessage: "Ce champ est obligatoire",
                }
            );
        }
        
        if(inputType !== 'hidden' && inputType !== 'submit') {
            try {
                validator.addField(`#${inputID}`, rules);
            } catch (error) {
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

/**
 * Send email with EmailJS
 * 
 * @param {*} data - Object containing the data to send
 * @param {*} test_error - Boolean to simulate an error (for testing purposes)
 * @param {*} error_type - String to specify the type of error to simulate (emailjs, fetch or left empty string for default)
 */
// async function sendEmail(data, test_error=false, error_type="") {
//     console.log("Sending email...");
    
//     // Define env variables
//     let serviceId, templateId, userId;

//     // get sensitive data from .env file
//     try {
//         //const sensitiveData = await fetchSensitiveData();
//         const sensitiveData = await getAPISecrets();

//         serviceId = sensitiveData.emailjs_service_id;
//         templateId = sensitiveData.emailjs_template_id;
//         userId = sensitiveData.emailjs_user_id;
//     } catch (error) {
//         throw new Error('Error getting sensitive data from server ', error);
//     }

//     // Simulate an error (for testing purposes), create switch on error_type
//     if(test_error) {
//         //console.error("Simulating an error for testing purposes");
//         switch(error_type) {
//             case "emailjs":
//                 // Mess with EmailJS service ID
//                 console.log("Simulating an error with EmailJS service ID");
//                 serviceId = "wrong_service_id_forTesting";
//                 break;
//             case "fetch":
//                 throw new Error('Error getting sensitive data from server ', error);
//                 break;
//             default:
//                 throw new Error('Error sending email: ', error);
//         }
//     }

//     // Send email with EmailJS
//     try {
//         const response = await emailjs.send(
//             serviceId, 
//             templateId, {
//                 to_email: "association@lesinvisibles.ch",
//                 from_email: data.email,
//                 subject: "Les Invisibles - Nouveau message",
//                 first_name: data.first_name,
//                 last_name: data.last_name,
//                 email: data.email,
//                 message: data.message,
//                 "g-recaptcha-response": data.recaptcha_token
//             }, 
//             userId
//         );
//         console.log('SUCCESS!', response.status, response.text);
//     }
//     catch(error) {
//         console.log(error);
//         throw error;
//     }

// }