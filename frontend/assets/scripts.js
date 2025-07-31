
let socket = io();
const messages = document.getElementById("messages");


socket.on("messages", (data) => {
    messages.innerHTML = '';
    data.forEach(msg => {
        messages.innerHTML += `<p>${msg}</p>`;
    });
})


const btn = document.getElementById("btn");
const txt = document.getElementById("txt");
btn.onclick = () => {
    socket.emit("msg", txt.value);
}
