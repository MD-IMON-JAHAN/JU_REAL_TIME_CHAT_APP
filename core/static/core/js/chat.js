document.addEventListener('DOMContentLoaded', function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + roomId + '/'
    );

    const chatContainer = document.getElementById('chat-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function addMessage(message, sender, timestamp, isCurrentUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isCurrentUser ? 'sent' : 'received'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;
        
        const infoDiv = document.createElement('div');
        infoDiv.className = 'message-info';
        infoDiv.textContent = `${sender} - ${timestamp}`;
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(infoDiv);
        
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const isCurrentUser = data.sender === currentUser;
        addMessage(data.message, data.sender, data.timestamp.split(' ')[1], isCurrentUser);
    };

    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender': currentUser
            }));
            messageInput.value = '';
        }
    });

    scrollToBottom();
});