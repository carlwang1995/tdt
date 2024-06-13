const photo = document.querySelector("#photo");
const order_title = document.querySelector("#order_title");
const order_cat = document.querySelector("#order_cat");
const order_mrt = document.querySelector("#order_mrt");
const attraction_des = document.querySelector("#des");
const attraction_adr = document.querySelector("#adr");
const attraction_traffic = document.querySelector("#traffic");
const left_arrow = document.querySelector("#left_photo");
const right_arrow = document.querySelector("#right_photo");
const fh_radio = document.querySelector("#first_half");
const sh_radio = document.querySelector("#second_half");
const order_price = document.querySelector("#price");
const circle = document.querySelector("#btn_circle");

// Fetch Attraction API
const get_attraction_info = async () => {
  let current_id = document.URL.split("/attraction/")[1];
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
    if (i == 0) {
      circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
    } else {
      circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
    }
  }
  photo.style.backgroundImage = `url(${data.images[photo_num]})`;
  right_arrow.addEventListener("click", () => {
    if (photo_num < data.images.length - 1) {
      photo_num++;
      circle.innerHTML = "";
      for (i = 0; i < data.images.length; i++) {
        if (i == photo_num) {
          circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
        } else {
          circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
        }
      }
    }
    photo.style.backgroundImage = `url(${data.images[photo_num]})`;
  });
  left_arrow.addEventListener("click", () => {
    if (photo_num > 0) {
      photo_num--;
      circle.innerHTML = "";
      for (i = 0; i < data.images.length; i++) {
        if (i == photo_num) {
          circle.innerHTML += `<img class="circle" src=${circle_current_src}/>`;
        } else {
          circle.innerHTML += `<img class="circle" src=${circle_blank_src}/>`;
        }
      }
    }
    photo.style.backgroundImage = `url(${data.images[photo_num]})`;
  });
};
get_attraction_info();

// Time Selection
fh_radio.addEventListener("click", () => {
  order_price.innerText = "新台幣2000元";
});
sh_radio.addEventListener("click", () => {
  order_price.innerText = "新台幣2500元";
});
