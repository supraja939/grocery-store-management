function login() {
    let user = {
        username: $("#username").val(),
        password: $("#password").val()
    };

    $.ajax({
        url: API_URL + "/login",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(user),
        success: function () {
            localStorage.setItem("loggedIn", "true");
            window.location.href = "index.html";
        },
        error: function () {
            $("#error").text("Invalid Username or Password");
        }
    });
}
