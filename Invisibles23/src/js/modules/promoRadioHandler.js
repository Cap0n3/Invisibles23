/**
 * Handles the selection of a radio button and displays appropriate alerts based on the selection.
 */
export function promoRadioHandler() {
    console.log("Checking sanity of promoRadioHandler");
    const memberAlertBox = document.getElementById('alert-box-member');
    const nonMemberAlertBox = document.getElementById('alert-box-non-member');
    const memberRadioButtons = document.querySelectorAll('#member-check input[type="radio"]');

    if ( !memberAlertBox || !nonMemberAlertBox || !memberRadioButtons) {
        console.error('Required elements not found');
        return;
    }

    memberRadioButtons.forEach(radio => radio.addEventListener('change', () => {
        // Get the selected radio button value
        const selectedRadioButton = [...memberRadioButtons].find(radio => radio.checked).value;
        // Display the appropriate alert box based on the selected
        if (selectedRadioButton === 'isMember') {
            memberAlertBox.classList.remove('d-none');
            nonMemberAlertBox.classList.add('d-none');
        }
        else if (selectedRadioButton === 'isNotMember') {
            nonMemberAlertBox.classList.remove('d-none');
            memberAlertBox.classList.add('d-none');
        }
        else {
            memberAlertBox.classList.add('d-none');
            nonMemberAlertBox.classList.add('d-none');
        }    
    }));

    // Clean up function
    return function() {
        console.log("Cleaning up event listeners");
        memberRadioButtons.forEach(radio => radio.removeEventListener('change', () => {}));
    }
}