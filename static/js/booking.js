const delete_booking = document.querySelector("#delete_booking");
const booking_welcome_box = document.querySelector("#booking_welcome");
const booking_loading = document.querySelector("#booking_loading");
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
const booking_confirm_btn = document.querySelector("#booking_confirm_btn");
const order_form = document.querySelector("#order_form");
const booking_input_username_error = document.querySelector(
  "#booking_input_username_error"
);
const booking_input_email_error = document.querySelector(
  "#booking_input_email_error"
);
const booking_input_phone_error = document.querySelector(
  "#booking_input_phone_error"
);

const emailRegxp =
  /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

// 定義滑鼠按下訂購動作
function event_mousedown_btn() {
  booking_confirm_btn.style.backgroundColor = "rgb(35, 71, 80)";
}
function event_mouseup_btn() {
  booking_confirm_btn.style.backgroundColor = "rgba(68, 136, 153, 1)";
}
function set_btn_state_finish() {
  booking_confirm_btn.type = "submit";
  booking_confirm_btn.style.backgroundColor = "rgba(68, 136, 153, 1)";
  booking_confirm_btn.addEventListener("mousedown", event_mousedown_btn);
  booking_confirm_btn.addEventListener("mouseup", event_mouseup_btn);
}
function set_btn_state_NOT_finish() {
  booking_confirm_btn.type = "button";
  booking_confirm_btn.style.backgroundColor = "rgb(220, 220, 220)";
  booking_confirm_btn.removeEventListener("mousedown", event_mousedown_btn);
  booking_confirm_btn.removeEventListener("mouseup", event_mouseup_btn);
}
// 訂購資料取得及渲染
const get_booking_info = async () => {
  let user_info_obj = await userAuth();
  let token = localStorage.getItem("token");
  if (token != null) {
    booking_user_name.innerText = user_info_obj.user_name;
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
    booking_user_name.innerText = user_info_obj.user_name;
    booking_input_username.value = user_info_obj.user_name;
    booking_input_email.value = user_info_obj.user_email;
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
    booking_box.forEach((e) => {
      e.style.display = "flex";
    });
    hr.forEach((h) => {
      h.style.display = "block";
    });
  } else if (data == null) {
    booking_box.forEach((e) => {
      e.style.display = "none";
    });
    hr.forEach((h) => {
      h.style.display = "none";
    });
    booking_no_data_box.style.display = "flex";
  }
  booking_loading.style.display = "none";
  booking_welcome_box.style.display = "flex";
  return data;
};
// 定義刪除行為
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
// 取消表單預設post行為
order_form.addEventListener("submit", (e) => {
  e.preventDefault();
});

// 畫面載入執行工作
window.addEventListener("load", async () => {
  let booking_info = await get_booking_info();
  if (!booking_info) {
    return;
  }
  let attraction = booking_info.attraction;
  let date = booking_info.date;
  let time = booking_info.time;
  let price = booking_info.price;
  let prime;

  // 定義按下訂購按鈕的行為
  function sent_order() {
    let input_check = true;
    if (booking_input_username.value == "") {
      input_check = false;
      booking_input_username_error.style.display = "block";
    } else {
      booking_input_username_error.style.display = "none";
    }
    if (
      booking_input_email.value == "" ||
      booking_input_email.value.search(emailRegxp) == -1
    ) {
      input_check = false;
      booking_input_email_error.style.display = "block";
    } else {
      booking_input_email_error.style.display = "none";
    }
    if (
      booking_input_phone.value == "" ||
      booking_input_phone.value.length != 10
    ) {
      input_check = false;
      booking_input_phone_error.style.display = "block";
    } else {
      booking_input_phone_error.style.display = "none";
    }

    if (!input_check) {
      return;
    }

    let data = {
      prime: prime,
      order: {
        price: price,
        trip: { attraction: attraction },
        date: date,
        time: time,
      },
      contact: {
        name: booking_input_username.value,
        email: booking_input_email.value,
        phone: booking_input_phone.value,
      },
    };

    let token = localStorage.getItem("token");

    if (
      data.contact.name != "" &&
      data.contact.email != "" &&
      data.contact.phone != ""
    ) {
      booking_confirm_btn.removeEventListener("click", sent_order);
      set_btn_state_NOT_finish();
      booking_confirm_btn.innerText = "確認中...";
      booking_confirm_btn.type = "button";
      booking_confirm_btn.style.backgroundColor = "rgb(220, 220, 220)";

      fetch("/api/orders", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          return response.json();
        })
        .then((result) => {
          if (!result.error) {
            fetch("/api/booking", {
              headers: {
                Authorization: `Bearer ${token}`,
              },
              method: "DELETE",
            })
              .then((response) => {
                return response.json();
              })
              .then((delete_result) => {
                if (delete_result.ok) {
                  location.href = `/thankyou?name=${result.data.number}`;
                } else {
                  return;
                }
              });
          }
        });
    }
  }
  // 更新訂購按鈕狀態、prime字串
  TPDirect.card.onUpdate((update) => {
    if (!update.canGetPrime) {
      booking_confirm_btn.removeEventListener("click", sent_order);
      set_btn_state_NOT_finish();
    } else if (update.canGetPrime) {
      booking_confirm_btn.addEventListener("click", sent_order);
      TPDirect.card.getPrime((result) => {
        if (result.status === 0) {
          prime = result.card.prime;
        }
      });
      set_btn_state_finish();
    }
  });
});
