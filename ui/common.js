const API_URL = "http://127.0.0.1:5000";
if (!localStorage.getItem("loggedIn") && !location.pathname.includes("login.html")) {
    window.location.href = "login.html";
}
function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "login.html";
}
