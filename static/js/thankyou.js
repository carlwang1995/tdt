const td_number = document.querySelector("#td_number");
const td_attraction_name = document.querySelector("#td_attraction_name");
const td_attraction_address = document.querySelector("#td_attraction_address");
const td_attraction_date = document.querySelector("#td_attraction_date");
const td_attraction_time = document.querySelector("#td_attraction_time");
const td_order_status = document.querySelector("#td_order_status");
const td_order_price = document.querySelector("#td_order_price");
const thank_btn = document.querySelector("#thank_btn");

userAuth();

let token = localStorage.getItem("token");
if (token === null) {
  location.href = "/";
}
let url = location.href;
let number = url.split("=")[1];

window.addEventListener("load", async () => {
  let request = await fetch(`/api/order/${number}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  let response = await request.json();
  let data = response.data;
  td_number.innerText = data.number;
  td_attraction_name.innerText = data.trip.attraction.name;
  td_attraction_address.innerText = data.trip.attraction.address;
  td_attraction_date.innerText = data.trip.date;
  if (data.trip.time == "morning") {
    td_attraction_time.innerText = "早上 9 點到下午 4 點";
  } else if (data.trip.time == "afternoon") {
    td_attraction_time.innerText = "下午 4 點到晚上 10 點";
  }
  if (data.status === 0) {
    td_order_status.innerText = "付款成功";
    td_order_status.style.color = "green";
  } else if (data.status === 1) {
    td_order_status.innerText = "付款失敗";
    td_order_status.style.color = "red";
  }
  td_order_price.innerText = data.price + " 元";
  thank_btn.addEventListener("click", () => {
    location.href = `/attraction/${data.trip.attraction.id}`;
  });
});
