const signin_up_btn = document.querySelector("#signin_up_btn");
const signout_btn = document.querySelector("#signout_btn");

const show_sign_in = () => {
  signin_up_btn.style.display = "block";
  signout_btn.style.display = "none";
};

const show_sign_out = () => {
  signin_up_btn.style.display = "none";
  signout_btn.style.display = "block";
};

let quick_check;
quick_check ? show_sign_in() : show_sign_out();

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
  if (response["data"] != null) {
    show_sign_out();
    quick_check = true;
    let user_info = {
      user_name: response.data.name,
      user_email: response.data.email,
    };
    return user_info;
  } else {
    show_sign_in();
    quick_check = false;
    signin_up_btn.style.display = "block";
    signout_btn.style.display = "none";
  }
};
