import JustValidate from 'just-validate';
import emailjs, { send } from '@emailjs/browser';
import { displayMessage } from './utils/helpers';

const nameRegex = /^[^#+*/()=?°§$£!%_;:<>]+$/;
const messageRegex = /^[^\[\]{}<>]+$/;

export function contactForm() {
    const validator = new JustValidate('#contactForm', 
        {
            successFieldCssClass: ['is-valid'], // CSS class to add when input is valid
            errorFieldCssClass: ['is-invalid'], // CSS class to add when input is invalid
            errorLabelCssClass: ['invalid-feedback'], // CSS class to add for error message
            validateBeforeSubmitting: false,
        }
    );

    validator
        .addField('#id_first_name', [
            {
                rule: "required",
                errorMessage: "Merci d'indiquer votre prénom",
            },
            {
                rule: 'minLength',
                value: 2,
                errorMessage: "Votre prénom doit contenir au moins 2 caractères",
            },
            {
                rule: 'maxLength',
                value: 50,
                errorMessage: "Votre prénom ne peut pas contenir plus de 50 caractères",
            },
            {
                rule: 'customRegexp',
                value: nameRegex,
                errorMessage: "Un caractère invalide a été détecté",
            },
        ])
        .addField('#id_last_name', [
            {
                rule: "required",
                errorMessage: "Merci d'indiquer votre nom",
            },
            {
                rule: 'minLength',
                value: 2,
                errorMessage: "Votre nom doit contenir au moins 2 caractères",
            },
            {
                rule: 'maxLength',
                value: 50,
                errorMessage: "Votre nom ne peut pas contenir plus de 50 caractères",
            },
            {
                rule: 'customRegexp',
                value: nameRegex,
                errorMessage: "Un caractère invalide a été détecté",
            },
        ])
        .addField('#id_email', [
            {
                rule: "required",
                errorMessage: "Merci d'indiquer votre adresse email",
            },
            {
                rule: "email",
                errorMessage: "Votre adresse email semble ne pas être valide",
            },
        ])
        .addField('#id_message', [
            {
                rule: "required",
                errorMessage: "Vous avez oublié d'écrire votre message",
            },
            {
                rule: 'minLength',
                value: 5,
                errorMessage: "Il semblerait que votre message soit un peu court",
            },
            {
                rule: 'maxLength',
                value: 10000,
                errorMessage: "Hum, votre message est un peu trop long (max 10'000 caractères)",
            },
            {
                rule: 'customRegexp',
                value: messageRegex,
                errorMessage: "Un caractère invalide a été détecté",
            },
        ])
        .onSuccess((form) => {handleSubmit(form)})
}

function handleSubmit(formObject) {
    // Get form input values and put them in an object
    const formData = {
        first_name: formObject.target.elements["first_name"].value,
        last_name: formObject.target.elements["last_name"].value,
        email: formObject.target.elements["email"].value,
        message: formObject.target.elements["message"].value,
    };

    sendEmail(formData)
    .then(function(response) {
        // Display success message
        displayMessage(
            formObject, 
            "Votre message a bien été envoyé", 
            {
                success: "#successMessage", 
                error: "#errorMessage"
            }, 
            "success"
        );
        console.log("SUCCESS!", response.status, response.text);
    })
    .catch(function(error) {
        // Display error message
        displayMessage(
            formObject, 
            "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site ...", 
            {
                success: "#successMessage",
                error: "#errorMessage"
            },
            "error"
        );
        console.log("FAILED...", error);
    });
}

function sendEmail(data) {
    return new Promise(function(resolve, reject) {
        // Get environment variables from .env file
        let serviceId = process.env.EMAILJS_SERVICE_ID;
        let templateId = process.env.EMAILJS_TEMPLATE_ID;
        let userId = process.env.EMAILJS_USER_ID;
        // Use EmailJS library or service to send the email
        emailjs.send(
            serviceId, 
            templateId, {
                to_email: "afra.amaya7@gmail.com",
                from_email: "test@dev_invisibles23.com",
                subject: "Test message for DEV",
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                message: data.message,
            }, 
            userId,
        )
        .then(function(response) {
            resolve(response); // Resolve the Promise when email is sent successfully
        })
        .catch(function(error) {
            reject(error); // Reject the Promise if there is an error in sending the email
        });
    });
}

// function displayMessage(formObject, statusMessage, type) {
//     // Code to display the message based on the type (success or error)
//     // Get current form
//     let currentForm = formObject.target;
//     // Get containers for success and error messages
//     let successContainer = currentForm.querySelector("#successMessage");
//     let errorContainer = currentForm.querySelector("#errorMessage");
//     // Get all inputs and convert to array
//     let inputs = Array.from(currentForm.querySelectorAll("input, textarea"));
    
//     if (type === "success") {
//         successContainer.innerHTML = statusMessage;
//         // Show success message
//         successContainer.classList.replace("hideMessage", "showMessage");
//         // Wait 2 seconds before resetting form and hiding success message
//         setTimeout(function() {
//             // Remove "is-valid" class from all inputs
//             inputs.forEach(input => input.classList.remove("is-valid"));
//             // Reset form
//             currentForm.reset();
//             // Hide success message
//             successContainer.classList.replace("showMessage", "hideMessage");
//         }, 5000);
//     }
//     else if (type === "error") {
//         // Set error message
//         errorContainer.innerHTML = statusMessage;
//         // Show error message
//         errorContainer.classList.replace("hideMessage", "showMessage");
//     }
// }