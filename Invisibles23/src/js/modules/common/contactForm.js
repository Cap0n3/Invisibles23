import JustValidate from 'just-validate';

const nameRegex = /^[^#+*/()=?°§$£!%_;:<>]+$/;
const messageRegex = /^[^\[\]{}<>]+$/;

export function contactForm() {
    const validator = new JustValidate('#contactForm', 
        {
            successFieldCssClass: ['is-valid'], // CSS class to add when input is valid
            errorFieldCssClass: ['is-invalid'], // CSS class to add when input is invalid
            errorLabelCssClass: ['invalid-feedback'], // CSS class to add for error message
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
}
