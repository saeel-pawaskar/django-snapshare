function registerValidation() {
    const email = document.getElementById('email').value.trim();
    const fullname = document.getElementById('fullname').value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();
    message = document.getElementById('message');

    // Clear previous error message
    message.innerHTML = "";

    if (username === "" || email === "" || password === "" || confirmPassword === "" || fullname === "") {
        message.innerHTML = "All fields are required.";
        return false;
    } else if (password !== confirmPassword) {
        message.innerHTML = "Passwords do not match.";
        return false;
    }

    return true;
}

// Attach validation to login form submission
document.getElementById('registerForm').addEventListener('submit', function(event) {
    console.log('Form submitted');
    if (!registerValidation()) {
        console.log('Validation failed');
        const errorBox = document.getElementById('errorBox');
        if (errorBox) {
            errorBox.style.display = 'block';
        }
        event.preventDefault(); // Ensure this prevents form submission
    }
});

