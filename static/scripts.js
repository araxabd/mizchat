
let socket = io();
const btn = document.getElementById("btn");
const txt = document.getElementById("txt");
const messages = document.getElementById("messages");
btn.onclick = () => {
    socket.emit("msg", txt.value);
}

socket.on("messages", (data) => {
    messages.innerHTML = '';
    data.forEach(msg => {
        messages.innerHTML += `<p>${msg}</p>`;
    });
})
