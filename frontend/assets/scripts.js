
async function authCheck() {
    try {
        const res = await fetch(`${DOMAIN}/is-authenticated`, {
            method: "GET",
            credentials: "include"
        });
        console.log(res);
        const data = await res.json();
        console.log(data);

        if(data.authenticated) {
            return {auth: true, uid: data.user_id};
        } else {
            return {auth: false, err: data.err};
        }
    } catch (error) {
        console.log(error)
        return {auth: false, err: "Error"};
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const authStatus = await authCheck();
console.log(authStatus)
    if (authStatus.auth) {
        document.getElementById("main").style.display = "block";
        document.getElementById("anonymous").style.display = "none";
    } else {
        if (authStatus.err) {
            console.log(authStatus.err);
        }
        window.location.href = "/login.html";
    }
});

// let socket = io();
// const messages = document.getElementById("messages");


// socket.on("messages", (data) => {
//     messages.innerHTML = '';
//     data.forEach(msg => {
//         messages.innerHTML += `<p>${msg}</p>`;
//     });
// })


// const btn = document.getElementById("btn");
// const txt = document.getElementById("txt");
// btn.onclick = () => {
//     socket.emit("msg", txt.value);
// }
