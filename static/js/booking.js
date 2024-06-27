const delete_booking = document.querySelector("#delete_booking");
const booking_user_name = document.querySelector("#booking_user_name");
const booking_info_title = document.querySelector(
  "#booking_content_detail_info_title"
);
const booking_photo = document.querySelector("#booking_content_detail_photo");
const booking_info_date = document.querySelector(
  "#booking_content_detail_info_data_date"
);
const booking_info_time = document.querySelector(
  "#booking_content_detail_info_data_time"
);
const booking_info_price = document.querySelector(
  "#booking_content_detail_info_data_price"
);
const booking_info_address = document.querySelector(
  "#booking_content_detail_info_data_address"
);
const booking_input_username = document.querySelector(
  "#booking_input_username"
);
const booking_input_email = document.querySelector("#booking_input_email");
const booking_input_phone = document.querySelector("#booking_input_phone");
const booking_confirm_price = document.querySelector("#booking_confirm_price");
const booking_box = document.querySelectorAll(".booking_box");
const booking_no_data_box = document.querySelector("#booking_no_data_box");
const hr = document.querySelectorAll(".hr");

window.addEventListener("load", async () => {
  let user_info_obj = await userAuth();
  let token = localStorage.getItem("token");
  if (token != null) {
    booking_user_name.innerText = user_info_obj.user_name;
    booking_input_username.value = user_info_obj.user_name;
    booking_input_email.value = user_info_obj.user_email;
  }
  let request = await fetch("/api/booking", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method: "GET",
  });
  let response = await request.json();
  if (
    response["error"] === true &&
    response["message"] === "未登入系統，拒絕存取"
  ) {
    location.href = "/";
  }
  let data = response["data"];
  if (data != null) {
    booking_photo.style.backgroundImage = `url(${data["attraction"]["image"]})`;
    booking_info_title.innerText = `台北一日遊：${data["attraction"]["name"]}`;
    booking_info_date.innerText = data["date"];
    booking_info_price.innerText = "新台幣 " + data["price"] + " 元";
    booking_info_address.innerText = data["attraction"]["address"];
    if (data["time"] == "morning") {
      booking_info_time.innerText = "早上 9 點到下午 4 點";
    } else if (data["time"] == "afternoon") {
      booking_info_time.innerText = "下午 4 點到晚上 10 點";
    }
    booking_confirm_price.innerText = "新台幣 " + data["price"] + " 元";
  } else if (data == null) {
    booking_box.forEach((e) => {
      e.style.display = "none";
    });
    hr.forEach((h) => {
      h.style.display = "none";
    });
    booking_no_data_box.style.display = "flex";
  }
});

delete_booking.addEventListener("click", async () => {
  let token = localStorage.getItem("token");
  let request = await fetch("/api/booking", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method: "DELETE",
  });
  let response = await request.json();
  if (response["ok"] === true) {
    location.reload();
  }
});
