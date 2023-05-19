import JustValidate from 'just-validate';
import emailjs from '@emailjs/browser';

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
        .onSuccess((form) => {handleFormSubmit(form)})
}

function handleFormSubmit(formObject) {
    // Get current form
    let currentForm = formObject.target;
    // Get containers for success and error messages
    let successContainer = currentForm.querySelector("#successMessage");
    let errorContainer = currentForm.querySelector("#errorMessage");
    // Get all inputs
    let inputs = currentForm.querySelectorAll("input, textarea");
    Array.from(inputs).forEach(input => input.blur());

    // Send email and get response
    if (sendEmail()) {
        // Show success message
        successContainer.classList.replace("hideMessage", "showMessage");
        // Wait 2 seconds before resetting form
        setTimeout(function() {
            // Remove "is-valid" class from all inputs
            Array.from(inputs).forEach(input => input.classList.remove("is-valid"));
            // Reset form
            currentForm.reset();
            // Hide success message
            successContainer.classList.replace("showMessage", "hideMessage");
        },5000);
    }
    else {
        console.log("ERROR");
        // Create error message
        let errorMessage = "Une erreur est survenue";
        errorContainer.innerHTML = errorMessage;
        // Show error message
        errorContainer.classList.replace("hideMessage", "showMessage");
    }
}

function sendEmail() {
    console.log("SENDING EMAIL");
    var templateParams = {
        name: 'James',
        notes: 'Check this out!'
    };
     
    emailjs.send('service_tjy46fw', 'template_xr7tydo', templateParams, 'iizyhd3n6xCNfKq-0')
        .then(function(response) {
           console.log('SUCCESS!', response.status, response.text);
        }, function(error) {
           console.log('FAILED...', error);
        });
    
    return true;
}
