export function contactForm() {
    'use strict'

    const forms = document.querySelectorAll('.contactForm');

    // Create an array and iterate over each element to add an event listener
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            // Add bootstrap 4 was-validated classes to trigger validation messages
            form.classList.add('was-validated')
        }, false)
    })


}