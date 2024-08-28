import JustValidate from 'just-validate';
import { displayMessage } from './utils/helpers';
import { addContactToList } from "./utils/api";

/**
 * Initialize the newsletter form.
 * @param {string} formID - The ID of the form
 * @returns {void}
 * 
 * @example
 * newsletterForm("newsletterFooter");
 */
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


/**
 * This function is called when the newsletter form is submitted.
 * It adds the email to the list of contacts.
 * 
 * @param {*} formObject 
 * @param {*} email 
 */
async function handleNewsletterSubmit(formObject, email) {
    const formID = formObject.target.id;
    const messageSelectors = {
        success: `#${formID}SuccessMessage`,
        warning: `#${formID}WarningMessage`,
        error: `#${formID}ErrorMessage`,
    };

    try {
        await addContactToList(email);
        displayMessage(formObject, "Votre adresse email a bien été ajoutée à la liste de diffusion. Merci !", messageSelectors, "success");
    } 
    catch (error) {
        const errorStatus = error.response ? error.response.status : null;
        let errorMessage = "Désolé, une erreur est survenue ! Réessayez plus tard et si le problème persiste, contactez l'administrateur du site.";
        let errorType = "error";

        if (errorStatus === 400) {
            errorMessage = "Cette adresse email est déjà inscrite à la liste de diffusion.";
            errorType = "warning";
        }

        displayMessage(formObject, errorMessage, messageSelectors, errorType);
    }
}