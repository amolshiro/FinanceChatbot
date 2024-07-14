async function sendMessage() {
    const input = document.getElementById("user-input");
    const age = document.getElementById("user-age").value;
    const chatArea = document.getElementById("chat-area");

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input.value, age: age })
    });
    const message = await response.json();

    // Display the user's message
    chatArea.innerHTML += '<div class="user-message">You: ' + input.value + '</div>';
    // Display the chatbot's response
    chatArea.innerHTML += '<div class="bot-message">Bot: ' + message + '</div>';

    input.value = ''; // Clear the input after sending
    document.getElementById("user-age").style.visibility = 'hidden'; // Hide age input after first use
}
