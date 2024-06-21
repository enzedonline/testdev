const form = document.getElementById('PostForm');
const payloadModal = new bootstrap.Modal(document.getElementById('payloadModal'))
const maxPayloadSize = Number(form.dataset.maxPayload); // 1024 * 1024; // For example, 1 MB

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
    payloadSize = payloadSize / (1024 * 1024);
    // Check if the payload size exceeds the limit
    if (payloadSize > maxPayloadSize) {
        form.querySelector('#payloadSize').textContent = Math.ceil(payloadSize * 10) / 10;
        form.querySelector('#maxPayloadSize').textContent = maxPayloadSize;
        payloadModal.show();
        return;
    }

    form.submit();
});
