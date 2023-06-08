document.getElementById("user-input").addEventListener("submit", sendMessage);

function sendMessage(event) {
    event.preventDefault();
    var userInput = document.getElementById("user-message").value;

    if (userInput.trim() === "") {
        return;
    }

    var messageContainer = document.createElement("div");
    var UserAvatar = 'https://cdn.pixabay.com/photo/2020/07/14/13/07/icon-5404125_1280.png';
    messageContainer.className = "message-container user";
    messageContainer.innerHTML = "<div class='avatar-container'><img src=" + UserAvatar + " alt='User Avatar' class='avatar user-avatar'></div><div class='message-box user-message'>" + userInput + "</div>";

    document.querySelector(".chat-messages").appendChild(messageContainer);
    document.getElementById("user-message").value = "";

    fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = data[0].text;
        var botAvatar = 'https://media.istockphoto.com/id/1250000899/vector/chat-bot-robot-avatar-in-circle-round-shape-isolated-on-white-background-stock-vector.jpg?s=612x612&w=0&k=20&c=xj8GkmfFYH_Frho_pJ0HL2dkDwbZAI0Of6KwKdVsh1s=';
        var messageContainer = document.createElement("div");
        messageContainer.className = "message-container bot";
        messageContainer.innerHTML = "<div class='avatar-container'><img src=" + botAvatar + " alt='Bot Avatar' class='avatar bot-avatar'></div><div class='message-box bot-message'>" + botResponse + "</div>";

        document.querySelector(".chat-messages").appendChild(messageContainer);

        var $messages = document.querySelector(".chat-messages");
        $messages.scrollTop = $messages.scrollHeight;
    });
}
