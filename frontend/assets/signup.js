const signupBtn = document.getElementById("signupbtn");
const usrnameInput = document.getElementById("username");
const passwdInput = document.getElementById("password");

signupBtn.addEventListener("click", async () => {
    const res = await fetch("http://localhost:5000/signup", {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: usrnameInput.value, password: passwdInput.value})
    });
    if(res.ok) {
        window.location.href = "login.html";
    } else {
        alert("Username is taken");
    }
})
