const loginBtn = document.getElementById("loginbtn");
const logoutBtn = document.getElementById("logoutbtn");
const usrnameInput = document.getElementById("username");
const passwdInput = document.getElementById("password");

loginBtn.addEventListener("click", async () => {
    const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: usrnameInput.value, password: passwdInput.value})
    });

    if (res.ok) {
        window.location.href = "index.html";
    } else {
        alert("Wrong!!");
    }
});

logoutBtn.addEventListener("click", async () => {
    await fetch("http://localhost:5000/logout", {
        method: "POST",
        credentials: "include"
    });
    window.location.href = "index.html";
});

