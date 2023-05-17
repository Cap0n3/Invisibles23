import JustValidate from 'just-validate';

export function contactForm() {
    const validator = new JustValidate('#contactForm');

    validator.addField('#id_email', [
        {
            rule: 'required',
        },
        {
            rule: 'required',
        },
        {
            rule: 'email',
        },
    ])

}

// JUST IN CASE

//     // follow doc : https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
//     const form = document.getElementById("contactForm");
//     const fname = document.getElementById("id_first_name");
//     const lname = document.getElementById("id_last_name");
//     const email = document.getElementById("id_email");

//     email.addEventListener("input", (event) => {
//         validateEmail(email);
//     });
// }

// function validateEmail(_email) {
//     // Each time the user types something, we check if the form fields are valid.
//     if (_email.validity.valid) {
//         // In case there is an error message visible, if the field
//         if (_email.classList.contains('is-invalid')){
//             console.log("Remove invalid")
//             _email.classList.remove('is-invalid');
//         }
//         console.log("Valid");
//         _email.classList.add('is-valid');

//     } else {
//         console.log("Not valid")
//         _email.classList.add('is-invalid')
//     }