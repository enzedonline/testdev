const form = document.getElementById('PostForm');
const payloadModal = new bootstrap.Modal(document.getElementById('payloadModal'))
const maxPayloadSize = Number(form.dataset.maxPayload); // 1024 * 1024; // For example, 1 MB

form.addEventListener('submit', (event) => {
    if ((maxPayloadSize ?? 0) > 0) {
        // estimate max overhead at 10kB
        const estimatedOverhead = 10240
        const payloadSize = (
            new TextEncoder().encode(
                new URLSearchParams(
                    new FormData(form)
                ).toString()
            ).length + estimatedOverhead
        ) / 1048576;

        // Check if the payload size exceeds the limit
        if (payloadSize > maxPayloadSize) {
            event.preventDefault();
            form.querySelector('#payloadSize').textContent = payloadSize.toFixed(1);
            form.querySelector('#maxPayloadSize').textContent = maxPayloadSize;
            payloadModal.show();
            return;
        }
    }
}, true);
