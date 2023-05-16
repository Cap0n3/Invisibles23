export function contactForm() {
    // follow doc : https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
    const form = document.getElementById("contactForm");
    const email = document.getElementById("id_email");

    email.addEventListener("input", (event) => {
        // Each time the user types something, we check if the
        // form fields are valid.
        
        if (email.validity.valid) {
            console.log("Valid")
            email.classList.remove('is-invalid') // if it was invalid before
            email.classList.add('is-valid')

        } else {
            console.log("Not valid")
            email.classList.add('is-invalid')
        }
    });
}
