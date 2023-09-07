let socket;  

document.getElementById("join_room_btn").addEventListener("click",()=>{
    connectToWebSocket();
})

document.getElementById("send_ms_btn").addEventListener("click",()=>{
    sendMessage();
})


function connectToWebSocket() {
    const roomNameInput = document.getElementById("roomName");
    const roomName = roomNameInput.value;
    const wsUrl = `ws://localhost:8000/ws/${roomName}`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log("チャット開始");
    };

    socket.onmessage = (event) => {
        const message = event.data;
        console.log(event.data);
        displayMessage(message);
    };
}

function sendMessage() {

    const messageInput = document.getElementById("message");
    const userNameInput = document.getElementById("userName");
    const message = messageInput.value;
    const userName = userNameInput.value;

    const dataToSend = {
        message: message,
        userName: userName
    };

    socket.send(JSON.stringify(dataToSend));
    messageInput.value = "";
}

const chatDiv = document.getElementById("chat");
function displayMessage(message) {
    const messageElement = document.createElement("p");
    messageElement.innerText = message;
    chatDiv.appendChild(messageElement);
}