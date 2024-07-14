const signin_up_btn = document.querySelector("#signin_up_btn");
const signout_btn = document.querySelector("#signout_btn");
const nav_user_future = document.querySelector("#user_future");

const show_sign_in = () => {
  signin_up_btn.style.display = "block";
  signout_btn.style.display = "none";
};

const show_sign_out = () => {
  signin_up_btn.style.display = "none";
  signout_btn.style.display = "block";
};

const userAuth = async () => {
  let token = localStorage.getItem("token");
  let request = await fetch("/api/user/auth", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  let response = await request.json();
  // 控制nav顯示
  nav_user_future.style.display = "flex";
  if (response["data"] != null) {
    show_sign_out();
    let user_info = {
      user_name: response.data.name,
      user_email: response.data.email,
    };
    return user_info;
  } else {
    show_sign_in();
    signin_up_btn.style.display = "block";
    signout_btn.style.display = "none";
  }
};
