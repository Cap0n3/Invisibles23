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