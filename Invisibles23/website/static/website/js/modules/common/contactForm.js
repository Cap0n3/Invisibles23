export function contactForm() {
    // follow doc : https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
    const form = document.getElementById("contactForm");
    const email = document.getElementById("id_email");

    email.addEventListener("input", (event) => {
        // Each time the user types something, we check if the
        // form fields are valid.
        
        if (email.validity.valid) {
            // In case there is an error message visible, if the field
            // is valid, we remove the error message.
            console.log("Not valid")
        } else {
            // If there is still an error, show the correct error
            console.log("Not valid")
        }
    });
}
