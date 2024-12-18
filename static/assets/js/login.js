function loginValidation() {
    const usernameOrEmail = document.getElementById('usernameOrEmail').value.trim();
    const password = document.getElementById('password').value.trim();
    const message = document.getElementById('message');

    // Clear previous error message
    message.innerHTML = "";

    if (usernameOrEmail === "" || password === "") {
        message.innerHTML = "Both fields are required.";
        return false;
    }

    return true;
}

// Attach validation to login form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    console.log('Form submitted');
    if (!loginValidation()) {
        console.log('Validation failed');
        const errorBox = document.getElementById('errorBox');
        if (errorBox) {
            errorBox.style.display = 'block';
        }
        event.preventDefault(); // Prevent form submission if validation fails
    }
});