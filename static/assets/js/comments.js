function commentValidation() {
    const comment = document.getElementById('comment').value.trim();

    if (comment === "") {
        return false;
    }

    return true;
}

// Attach validation to login form submission
document.getElementById('commentForm').addEventListener('submit', function(event) {
    console.log('Form submitted');
    if (!commentValidation()) {
        console.log('Validation failed');
        event.preventDefault(); // Prevent form submission if validation fails
    }
});