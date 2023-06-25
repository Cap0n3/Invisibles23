import JustValidate from 'just-validate';
import { displayMessage } from './utils/helpers';
import { addContactToList } from "./utils/api";

export function newsletterForm(formID) {
    const inputID = `email-${formID}`;
    const validator = new JustValidate(`#${formID}`,
        {
            successFieldCssClass: ['is-valid'], // CSS class to add when input is valid
            errorFieldCssClass: ['is-invalid'], // CSS class to add when input is invalid
            errorLabelCssClass: ['invalid-feedback'], // CSS class to add for error message
            validateBeforeSubmitting: false,
            errorLabelCssClass: ['custom-invalid'],
        }
    );

    validator
        .addField(`#${inputID}`, [
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
            handleNewsletterSubmit(form, form.target.elements[inputID].value);
        }
        )
}

function handleNewsletterSubmit(formObject, email) {
    const formID = formObject.target.id;

    console.log(`#${formID}SuccessMessage`)
    
    addContactToList(email)
    .then((response) => {
        //console.log(response);
        displayMessage(
            formObject, 
            "Votre adresse email a bien été ajoutée à la liste de diffusion. Merci !",
            {
                success: `#${formID}SuccessMessage`,
                error: `#${formID}ErrorMessage`,
            },
            "success" 
        );
    })
    .catch((error) => {
        console.log(error);
        displayMessage(
            formObject, 
            "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site.",
            {
                success: `#${formID}SuccessMessage`,
                error: `#${formID}ErrorMessage`,
            },
            "error" 
        );
    }
    );
}