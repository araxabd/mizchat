
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
        window.location.href = "/login";
    }
});


const openCreateModal = document.getElementById("createbtn");
const closeCreateModal = document.getElementById("createclose");
const openJoinModal = document.getElementById("joinbtn");
const closeJoinModal = document.getElementById("joinclose");
const shadowBox = document.getElementById("shadow");
const createModal = document.getElementById("createmodal");
const joinModal = document.getElementById("joinmodal");


openCreateModal.addEventListener("click", () => {
    shadowBox.style.display = "block";
    createModal.style.display = "block";
});

closeCreateModal.addEventListener("click", () => {
    shadowBox.style.display = "none";
    createModal.style.display = "none";
});


openJoinModal.addEventListener("click", () => {
    shadowBox.style.display = "block";
    joinModal.style.display = "block";
});

closeJoinModal.addEventListener("click", () => {
    shadowBox.style.display = "none";
    joinModal.style.display = "none";
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
