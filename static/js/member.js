const member_name = document.querySelector("#member_name");
const member_email = document.querySelector("#member_email");
const order_table = document.querySelector("#member_booking_history_table");
const tr_nodata = document.querySelector("#tr_nodata");
const page_loading = document.querySelector("#page_loading");
const main_content = document.querySelector("#main_content");
const dialog_container_edit_memberInfo = document.querySelector(
  "#dialog_container_edit_memberInfo"
);
const dialog_edit_err_msg = document.querySelector("#edit_err");
const dialog_edit_sucess_msg = document.querySelector("#edit_sucess");
const input_edit_username = document.querySelector("#input_edit_username");
const input_edit_email = document.querySelector("#input_edit_email");
const edit_btn = document.querySelector("#btn_save_member_data");
const close_dialog_btn = document.querySelector("#close_edit_dialog");
const member_img_edit = document.querySelector("#member_img_edit");
const dialog_container_edit_memberImg = document.querySelector(
  "#dialog_container_edit_memberImg"
);
const input_file = document.querySelector("#input_file");
const firstlook_img = document.querySelector("#firstlook_img");
const btn_upload_img = document.querySelector("#btn_upload_img");
const member_img = document.querySelector("#img");

let token = localStorage.getItem("token");
if (token === null) {
  location.href = "/";
}

// 取得訂單資料 Function
async function get_booking_data(email) {
  let response = await fetch(`/api/orders/${email}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method: "GET",
  });
  let result = await response.json();
  return result;
}

// 生成歷史資料Table Function
function create_booking_table(num, price, status) {
  let t_row = document.createElement("tr");
  let t_data_num = document.createElement("td");
  let t_data_price = document.createElement("td");
  let t_data_status = document.createElement("td");
  t_row.className = "booking_row";
  t_row.addEventListener("click", () => {
    location.href = `/thankyou?name=${num}`;
  });
  t_data_num.innerText = num;
  t_data_price.innerText = price + " 元";
  if (status === 0) {
    t_data_status.innerText = "付款完成";
    t_data_status.style.color = "green";
  } else if (status === 1) {
    t_data_status.innerText = "付款失敗";
    t_data_status.style.color = "red";
  }
  order_table.appendChild(t_row);
  t_row.appendChild(t_data_num);
  t_row.appendChild(t_data_price);
  t_row.appendChild(t_data_status);
}

// 編輯會員資料Function
function open_edit_dialog() {
  dialog_window.style.display = "block";
  dialog_container_edit_memberInfo.style.top = "80px";
}

function close_edit_dialog() {
  dialog_window.style.display = "none";
  dialog_container_edit_memberInfo.style.top = "-400px";
  dialog_edit_err_msg.innerText = "";
  dialog_edit_sucess_msg.innerText = "";
}

// 顯示及隱藏編輯圖片圖示
function show_img_edit() {
  member_img_edit.style.display = "flex";
}
function hide_img_edit() {
  member_img_edit.style.display = "none";
}
// 更換大頭貼
function open_edit_img_dialog() {
  dialog_window.style.display = "block";
  dialog_container_edit_memberImg.style.top = "80px";
}

function close_edit_img_dialog() {
  dialog_window.style.display = "none";
  dialog_container_edit_memberImg.style.top = "-400px";
  // dialog_edit_err_msg.innerText = "";
  // dialog_edit_sucess_msg.innerText = "";
}

// 更新大頭貼
async function update_member_image(email) {
  let response = await fetch(`/api/upload/${email}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  let result = await response.json();
  let url = result.data;
  member_img.src = "/" + url;
}

window.addEventListener("load", async () => {
  main_content.style.display = "none";
  let user_info = await userAuth();
  [member_name.innerText, member_email.innerText] = [
    user_info.user_name,
    user_info.user_email,
  ];
  input_edit_username.value = user_info.user_name;
  input_edit_username.placeholder = user_info.user_name;
  input_edit_email.value = user_info.user_email;
  input_edit_email.placeholder = user_info.user_email;
  let order_info = await get_booking_data(user_info.user_email);
  if (order_info.data.length === 0) {
    tr_nodata.style.display = "";
  } else {
    tr_nodata.style.display = "none";
    for (i = 0; i < order_info.data.length; i++) {
      create_booking_table(
        order_info.data[i].number,
        order_info.data[i].order_price,
        order_info.data[i].status
      );
    }
  }
  page_loading.style.display = "none";
  main_content.style.display = "block";

  await update_member_image(user_info.user_email);

  edit_btn.addEventListener("click", async () => {
    let edit_info = {
      old_name: user_info.user_name,
      old_email: user_info.user_email,
      new_name: input_edit_username.value,
      new_email: input_edit_email.value,
    };
    if (
      edit_info.old_name == edit_info.new_name &&
      edit_info.old_email == edit_info.new_email
    ) {
      dialog_edit_err_msg.innerText = "";
      dialog_edit_sucess_msg.innerText = "會員資料未變更";
      return;
    }
    let request = await fetch("/api/edit_member", {
      headers: {
        Authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
      method: "PATCH",
      body: JSON.stringify(edit_info),
    });
    let response = await request.json();
    console.log(response);
    if (response.error === true) {
      dialog_edit_sucess_msg.innerText = "";
      dialog_edit_err_msg.innerText = response.message;
    } else if (response.ok === true) {
      input_edit_username.setAttribute("readonly", true);
      input_edit_email.setAttribute("readonly", true);
      input_edit_username.style.color = "white";
      input_edit_email.style.color = "white";
      input_edit_username.style.backgroundColor = "rgba(0, 0, 0, 0.2)";
      input_edit_email.style.backgroundColor = "rgba(0, 0, 0, 0.2)";
      dialog_edit_err_msg.innerText = "";
      dialog_edit_sucess_msg.innerText = "會員資料修改成功，請重新登入帳號";
      close_dialog_btn.style.display = "none";
      localStorage.removeItem("token");
      edit_btn.innerText = "登出系統";
      edit_btn.addEventListener("click", () => {
        location.href = "/";
      });
    }
  });
});

function load_file(file) {
  if (input_file.files[0]) {
    const reader = new FileReader();
    reader.onload = () => {
      firstlook_img.src = reader.result;
    };
    reader.readAsDataURL(file.target.files[0]);
  } else {
    firstlook_img.src = "/static/images/icon/user.png";
    return;
  }
}

input_file.addEventListener("change", (e) => {
  load_file(e);
});

btn_upload_img.addEventListener("click", async () => {
  let file = input_file.files[0];
  if (!file) {
    alert("請選擇上傳檔案");
    return;
  }
  const formData = new FormData();
  formData.append("file", file);
  let response = await fetch("/api/upload", {
    method: "POST",
    body: formData,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  let result = await response.json();
  if (result.ok === true) {
    alert("圖片上傳成功");
    location.reload();
  } else if (result.error === true) {
    alert("圖片上傳失敗");
  }
});
