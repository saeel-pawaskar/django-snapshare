function postValidation() {
    const image = document.getElementById('image').files.length;
    const video = document.getElementById('video').files.length;
    const message = document.getElementById('message');

    // Clear previous error message
    message.innerHTML = "";

    // Check if either image or video is selected
    if (image === 0 && video === 0) {
        message.innerHTML = "Image or Video is needed to create a post";
        return false;
    }

    return true;
}


document.getElementById('postForm').addEventListener('submit', function(event) {
    console.log('Form submitted');
    if (!postValidation()) {
        console.log('Validation failed');
        const errorBox = document.getElementById('errorBox');
        if (errorBox) {
            errorBox.style.display = 'block';
        }
        event.preventDefault(); // Prevent form submission if validation fails
    }
});