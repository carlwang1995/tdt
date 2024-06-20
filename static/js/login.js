let dialog_window = document.querySelector("#window_container");
let dialog_signin = document.querySelector("#signin_content");
let dialog_signup = document.querySelector("#signup_content");
let dialog_signin_err_msg = document.querySelector("#signin_err");
let dialog_signup_err_msg = document.querySelector("#signup_err");
let dialog_signup_sucess_msg = document.querySelector("#signup_sucess");
let signin_btn = document.querySelector("#btn_signin");
let signin_email_input = document.querySelector("#input_siginin_email");
let signin_password_input = document.querySelector("#input_siginin_password");
let signUp_btn = document.querySelector("#btn_signup");
let signUp_name_input = document.querySelector("#input_siginup_name");
let signUp_email_input = document.querySelector("#input_siginup_email");
let signUp_password_input = document.querySelector("#input_siginup_password");
let signin_up = document.querySelector("#signin_up_btn");
let signout = document.querySelector("#signout_btn");

function open_dialog() {
  dialog_window.style.display = "block";
}

function close_dialog() {
  dialog_signin.style.display = "flex";
  dialog_signup.style.display = "none";
  dialog_window.style.display = "none";
  dialog_signin_err_msg.innerText = "";
  dialog_signup_err_msg.innerText = "";
  dialog_signup_sucess_msg.innerText = "";
  signin_email_input.value = "";
  signin_password_input.value = "";
  signUp_name_input.value = "";
  signUp_email_input.value = "";
  signUp_password_input.value = "";
}
function change_to_signup() {
  signin_email_input.value = "";
  signin_password_input.value = "";
  dialog_signin.style.display = "none";
  dialog_signup.style.display = "flex";
  dialog_signin_err_msg.innerText = "";
  dialog_signup_sucess_msg.innerText = "";
}
function change_to_signin() {
  signUp_name_input.value = "";
  signUp_email_input.value = "";
  signUp_password_input.value = "";
  dialog_signin.style.display = "flex";
  dialog_signup.style.display = "none";
  dialog_signup_err_msg.innerText = "";
  dialog_signup_sucess_msg.innerText = "";
}
function signOUT() {
  localStorage.removeItem("token");
  location.reload();
}

// 註冊帳號
signUp_btn.addEventListener("click", async () => {
  let request = await fetch("/api/user", {
    body: JSON.stringify({
      name: signUp_name_input.value,
      email: signUp_email_input.value,
      password: signUp_password_input.value,
    }),
    headers: { "Content-Type": "application/json" },
    method: "POST",
  });
  let result = await request.json();
  if (result["error"] != true) {
    signUp_name_input.value = "";
    signUp_email_input.value = "";
    signUp_password_input.value = "";
    dialog_signup_err_msg.innerText = "";
    dialog_signin.style.display = "flex";
    dialog_signup.style.display = "none";
    dialog_signup_sucess_msg.innerText = "註冊成功！請重新登入。";
  } else {
    dialog_signup_err_msg.innerText = result["message"];
    dialog_signup_sucess_msg.innerText = "";
  }
});

// 登入帳號
signin_btn.addEventListener("click", async () => {
  let request = await fetch("/api/user/auth", {
    body: JSON.stringify({
      email: signin_email_input.value,
      password: signin_password_input.value,
    }),
    headers: { "Content-Type": "application/json" },
    method: "PUT",
  });
  let result = await request.json();
  if (result["error"] != true) {
    localStorage.setItem("token", result["token"]);
    location.reload();
  } else {
    dialog_signin_err_msg.innerText = result["message"];
    dialog_signup_sucess_msg.innerText = "";
  }
});

// 驗證登入狀態
window.addEventListener("load", async () => {
  token = localStorage.getItem("token");
  let request = await fetch("/api/user/auth", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  let result = await request.json();
  if (result["data"] != null) {
    signin_up.style.display = "none";
    signout.style.display = "block";
  } else {
    signin_up.style.display = "block";
    signout.style.display = "none";
  }
});
