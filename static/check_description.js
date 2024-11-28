function checkAndSubmit() {
    const usageDescription = document.getElementById('usage_description').value.trim();

    // Check if the text field is empty
    if (!usageDescription) {
        alert("Please describe your everyday use of the computer before proceeding.");
        return; // Do not submit the form
    }

    // Confirm if the user is sure
    const userConfirmed = confirm("Are you sure you have completed the text field to your satisfaction?");
    if (userConfirmed) {
        // Submit the form if confirmed
        document.querySelector('form').submit();
    }
}
