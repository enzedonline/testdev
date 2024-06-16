document.addEventListener("DOMContentLoaded", () => {localiseDates("localise-date")});
const scrollToId = (id) => {
    const postElement = document.getElementById(id);
    if (postElement) {
        postElement.scrollIntoView();
    }
}
const copyPostUrl = (url) => {
    navigator.clipboard.writeText(url)
        .then(() => {
            const copyToast = document.getElementById('copyToast');
            if (!!copyToast) {
                toastCopiedMsg = bootstrap.Toast.getOrCreateInstance(copyToast);
            }
            toastCopiedMsg.show();
        })
        .catch((error) => {
            console.error('Failed to copy URL to clipboard: ', error);
        });
}  