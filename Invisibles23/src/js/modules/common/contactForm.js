import JustValidate from 'just-validate';
import emailjs, { send } from '@emailjs/browser';
import { displayMessage } from './utils/helpers';

const nameRegex = /^[^#+*/()=?°§$£!%_;:<>]+$/;
const messageRegex = /^[^\[\]{}<>]+$/;

export function contactForm(formID) {
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

    validator.onSuccess((form) => {
        handleSubmit(form);
    });
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
            "Votre message a bien été envoyé. Merci !", 
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
            "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site.", 
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