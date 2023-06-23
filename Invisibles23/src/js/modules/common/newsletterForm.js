import JustValidate from 'just-validate';
import { displayMessage } from './utils/helpers';
import { addContactToList } from "./utils/api";

export function newsletterForm() {
    const validator = new JustValidate('#newsletterForm',
        {
            successFieldCssClass: ['is-valid'], // CSS class to add when input is valid
            errorFieldCssClass: ['is-invalid'], // CSS class to add when input is invalid
            errorLabelCssClass: ['invalid-feedback'], // CSS class to add for error message
            validateBeforeSubmitting: false,
        }
    );

    validator
        .addField('#id_newsletterEmail', [
            {
                rule: "required",
                errorMessage: "Merci d'indiquer votre adresse email",
            },
            {
                rule: 'email',
                errorMessage: "Merci d'indiquer une adresse email valide",
            },
        ])
        .onSuccess((form) => {
            // If the form is valid, we add the contact to the list
            handleNewsletterSubmit(form);
            //addContactToList(form.target.elements["email"].value);
        }
        )
}

function handleNewsletterSubmit(formObject) {
    console.log(formObject.target.elements["id_newsletterEmail"].value);
    displayMessage(
        formObject, 
        "Votre adresse email a bien été ajoutée à la liste de diffusion",
        {
            success: "#newsletterSuccessMessage",
            error: "#newsletterErrorMessage",
        },
        "success" 
    );
    //addContactToList(form.target.elements["id_newsletterEmail"].value);
}

// function displayNewsletterMessage(formObject, statusMessage, type) {
//     const successContainer = document.querySelector('#newsletterSuccessMessage');
//     const errorContainer = document.querySelector('#newsletterErrorMessage');
//     const currentForm = formObject.target;
//     // Get all inputs and convert to array
//     let inputs = Array.from(currentForm.querySelectorAll("input, textarea"));

//     if (type === "success") {
//         console.log("success")
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