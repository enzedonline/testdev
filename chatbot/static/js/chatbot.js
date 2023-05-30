const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');

messageForm.addEventListener('submit', (event) => {
    // prevent page refresh
    event.preventDefault();

    // if nothing entered, do nothing
    const message = messageInput.value.trim();
    if (message.length === 0) {
        return;
    }

    // add entered message to list
    const messageItem = document.createElement('li');
    messageItem.classList.add('message');
    messageItem.innerHTML = `
        <div class="message-text sent">
            <div class="message-sender">
                <b>You</b>
            </div>
            <div class="message-content">${message}</div>
        </div>`;
    messagesList.appendChild(messageItem);

    // add response container 
    // show spinner whail waiting for response from ai
    const responseContainer = document.createElement('li');
    responseContainer.classList.add('message');
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-text', 'received');
    const messageSender = document.createElement('div');
    messageSender.classList.add('message-sender');
    messageSender.innerHTML = "<b>AI Chatbot</b>"
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.innerHTML = `<div class="message-spinner"></div>`
    messageContainer.appendChild(messageSender);
    messageContainer.appendChild(messageContent);
    responseContainer.appendChild(messageContainer);
    messagesList.appendChild(responseContainer);
    responseContainer.scrollIntoView(true);


    // clear input form
    messageInput.value = '';

    // send message to api
    fetch('', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'message': message
        })
    })
    // parse response json
    .then(response => response.json())
    // add response in formatted element
    .then(data => {
        const response = data.response;
        messageContent.innerText = `${response}`
        responseContainer.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
    });
});

