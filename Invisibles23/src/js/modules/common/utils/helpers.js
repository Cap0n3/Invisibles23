/**
 * Function to expand text with a toggle link to show more or less text.
 * 
 * @param {*} textWrapperClass - The class of the wrapper of the text to expand
 * @param {*} limit - The number of words to show before the toggle link
 */
export function expandText(textWrapperClass, limit = 20) {
    const wrappers = document.querySelectorAll(`.${textWrapperClass}`);

    wrappers.forEach((wrapper, index) => {
        let isExpanded = false;
        const fullText = wrapper.innerText;

        // get paragraph of the wrapper with the text
        const paragraph = wrapper.querySelector('p');


        // Count number of words
        const wordCount = fullText.split(" ").length;

        // If the text is shorter than the limit, do nothing
        if (wordCount <= limit) {
            return;
        }
        
        // Extract the first 20 words and add "..." at the end
        const words = fullText.split(" ");
        let excerpt = words.slice(0, limit).join(" ");
        excerpt += " ...";
        paragraph.innerText = excerpt;

        // Create the toggle link
        const toggleLink = document.createElement("a");
        toggleLink.setAttribute("class", "ressource-toggle");
        toggleLink.innerText = "Voir plus";
        
        // Add the toggle link after the text
        paragraph.appendChild(toggleLink);

        // Add event listener to the toggle link
        toggleLink.addEventListener("click", toggleText);

        // Function to toggle the visibility of the full text
        function toggleText() {
            if (isExpanded) {
                // Show the excerpt
                paragraph.innerText = excerpt;
                paragraph.appendChild(toggleLink);
                toggleLink.innerText = "Voir plus";
            } else {
                // add text to the paragraph
                paragraph.innerText = fullText;
                // Show the full text
                //wrapper.innerText = fullText;
                paragraph.appendChild(toggleLink);
                toggleLink.innerText = "Voir moins";
            }
            isExpanded = !isExpanded;
        }
    })
}

/**
 * Function to display a message on the form. 
 * It will display a success message if the form was submitted successfully, or an error message if there was an error.
 * 
 * @param {Object} formObject - The form object
 * @param {String} statusMessage - The message to display
 * @param {Object} containersID - The IDs of the containers for the success and error messages
 * @param {String} type - The type of message (success or error)
 * @returns {void}
 * 
 * @example
 * // Display a success message
 * displayMessage(formObject, "Votre message a bien été envoyé.", {success: "#success-message", error: "#error-message"}, "success"); 
 * 
 * // Display an error message
 * displayMessage(formObject, "Une erreur est survenue. Veuillez réessayer plus tard.", {success: "#success-message", error: "#error-message"}, "error");
 */
export function displayMessage(formObject, statusMessage, containersID, type) {
    // Code to display the message based on the type (success or error)
    // Get current form
    const currentForm = formObject.target;
    // Get containers for success and error messages
    let successContainer = currentForm.querySelector(containersID.success);
    let errorContainer = currentForm.querySelector(containersID.error);
    // Get all inputs and convert to array
    let inputs = Array.from(currentForm.querySelectorAll("input, textarea"));

    if (type === "success") {
        successContainer.innerHTML = statusMessage;
        // Show success message
        successContainer.classList.replace("hideMessage", "showMessage");
        // Wait 2 seconds before resetting form and hiding success message
        setTimeout(function() {
            // Remove "is-valid" class from all inputs
            inputs.forEach(input => input.classList.remove("is-valid"));
            // Reset form
            currentForm.reset();
            // Hide success message
            successContainer.classList.replace("showMessage", "hideMessage");
        }, 5000);
    }
    else if (type === "error") {
        // Set error message
        errorContainer.innerHTML = statusMessage;
        // Show error message
        errorContainer.classList.replace("hideMessage", "showMessage");
        setTimeout(function() {
            // Remove "is-valid" class from all inputs
            inputs.forEach(input => input.classList.remove("is-valid"));
            // Reset form
            currentForm.reset();
            // Hide success message
            errorContainer.classList.replace("showMessage", "hideMessage");
        }, 5000);
    }
}