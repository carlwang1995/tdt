let userAuth = async () => {
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
    signin_up.style.display = "none";
    signout.style.display = "block";
    let user_info = {
      user_name: response.data.name,
      user_email: response.data.email,
    };
    return user_info;
  } else {
    signin_up.style.display = "block";
    signout.style.display = "none";
  }
};
