const photo = document.querySelector("#photo");
const order_title = document.querySelector("#order_title");
const order_cat = document.querySelector("#order_cat");
const order_mrt = document.querySelector("#order_mrt");
const order_form = document.querySelector("#order_form");
const order_date = document.querySelector("#order_date");
const strat_order_btn = document.querySelector("#strat_order_btn");
const attraction_des = document.querySelector("#des");
const attraction_adr = document.querySelector("#adr");
const attraction_traffic = document.querySelector("#traffic");
const left_arrow = document.querySelector("#left_photo");
const right_arrow = document.querySelector("#right_photo");
const fh_radio = document.querySelector("#first_half");
const sh_radio = document.querySelector("#second_half");
const order_price = document.querySelector("#price");
const circle = document.querySelector("#btn_circle");
const photo_order_contentBox = document.querySelector("#photo_order");
const attraction_contentBox = document.querySelector("#attraction_content");
const hr = document.querySelectorAll(".hr");
const attraction_loading = document.querySelector("#attraction_loading");

const current_id = document.URL.split("/attraction/")[1];

function get_today_date() {
  let Today = new Date();
  let yyyy = Today.getFullYear();
  let mm =
    Today.getMonth() + 1 >= 10
      ? Today.getMonth() + 1
      : "0" + (Today.getMonth() + 1);
  let dd = Today.getDate() >= 10 ? Today.getDate() : "0" + Today.getDate();
  let current_date = yyyy + "-" + mm + "-" + dd;
  return current_date;
}

// 驗證登入狀態 api/user/auth
userAuth();

// Fetch Attraction API
const get_attraction_info = async () => {
  let response = await fetch(`/api/attraction/${current_id}`);
  let result = await response.json();
  let data = result.data;
  let photo_num = 0;
  let data_arr = [
    data.name,
    data.category,
    data.mrt,
    data.description,
    data.address,
    data.transport,
  ];
  [
    order_title.innerText,
    order_cat.innerText,
    order_mrt.innerText,
    attraction_des.innerText,
    attraction_adr.innerText,
    attraction_traffic.innerText,
  ] = data_arr;

  // Image Slideshow
  let circle_blank_src = "/static/images/icon/circle.png";
  let circle_current_src = "/static/images/icon/circle_current.png";
  for (i = 0; i < data.images.length; i++) {
    let photo_img = document.createElement("div");
    photo_img.className = "photo_img fade";
    photo_img.style.backgroundImage = `url(${data.images[i]})`;
    photo.appendChild(photo_img);
    if (i == 0) {
      circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
    } else {
      circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
    }
  }
  const photo_imgs = document.querySelectorAll(".photo_img");
  photo_imgs[photo_num].style.display = "block";

  // right_arrow_button
  right_arrow.addEventListener("click", () => {
    if (photo_num < data.images.length - 1) {
      photo_num++;
    } else if (photo_num == data.images.length - 1) {
      photo_num = 0;
    }
    circle.innerHTML = "";
    for (i = 0; i < data.images.length; i++) {
      if (i == photo_num) {
        circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
      } else {
        circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
      }
    }
    photo_imgs.forEach((e) => {
      e.style.display = "none";
    });
    photo_imgs[photo_num].style.display = "block";
  });

  // left_arrow_button
  left_arrow.addEventListener("click", () => {
    if (photo_num > 0) {
      photo_num--;
    } else if (photo_num == 0) {
      photo_num = data.images.length - 1;
    }
    circle.innerHTML = "";
    for (i = 0; i < data.images.length; i++) {
      if (i == photo_num) {
        circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
      } else {
        circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
      }
    }
    photo_imgs.forEach((e) => {
      e.style.display = "none";
    });
    photo_imgs[photo_num].style.display = "block";
  });
  photo_order_contentBox.style.display = "flex";
  attraction_contentBox.style.display = "block";
  hr.forEach((hr) => {
    hr.style.display = "block";
  });
  attraction_loading.style.display = "none";
  return "loading_done";
};
get_attraction_info();

// Time Selection
let price = 2000;
let time_value = "morning";
fh_radio.addEventListener("click", () => {
  order_price.innerText = "新台幣2000元";
  price = 2000;
  time_value = "morning";
});
sh_radio.addEventListener("click", () => {
  order_price.innerText = "新台幣2500元";
  price = 2500;
  time_value = "afternoon";
});

// Post Attraction Booking
// 因為post需要加header，HTML的form的post方法無法夾帶header，要從JS中設定，所以在form發生submit時，先阻止他執行(只用來檢查order_date是否填寫)，由JS來post
order_form.addEventListener("submit", (e) => {
  e.preventDefault();
});
strat_order_btn.addEventListener("click", async () => {
  token = localStorage.getItem("token");
  if (!token) {
    open_dialog();
    strat_order_btn.type = "button";
    return;
  } else {
    close_dialog();
    strat_order_btn.type = "submit";
  }

  // 檢查日期
  let order_date_value = order_date.value;
  let today = get_today_date();
  if (order_date_value == "") {
    order_date.setCustomValidity("請選擇預定日期");
    return;
  } else if (order_date_value <= today) {
    order_date.setCustomValidity("日期無效，請選擇今天以後的日期");
    return;
  }

  booking_input = {
    id: current_id,
    date: order_date_value,
    time: time_value,
    price: price,
  };
  let request = await fetch("/api/booking", {
    headers: {
      Authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(booking_input),
    method: "POST",
  });
  let response = await request.json();
  if (response["ok"] == true) {
    location.href = "/booking";
  }
});
