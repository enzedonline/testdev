const form = document.getElementById('PostForm');

form.addEventListener('submit', (event) => {
    // Prevent the form from submitting immediately
    event.preventDefault();

    // Calculate the payload size
    const formData = new FormData(form);
    let payloadSize = 0;

    for (const [key, value] of formData.entries()) {
        // Calculate the size of each key-value pair
        payloadSize += key.length + value.length;
    }

    // Optionally, you can also add the size of other form elements, e.g., file inputs

    // Check if the payload size exceeds a certain limit
    const maxPayloadSize = 1024 * 1024; // For example, 1 MB
    if (payloadSize > maxPayloadSize) {
        alert('Payload size exceeds the limit. Please reduce the size.');
        return;
    }

    // If the payload size is within the limit, you can submit the form
    form.submit();
});
