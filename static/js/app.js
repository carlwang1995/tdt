let attractions = document.querySelector("#attractions");
let filter = document.querySelector("#attraction_filter");
let btn = document.querySelector("#search_btn");
let left_btn = document.querySelector("#left");
let right_btn = document.querySelector("#right");
let mrt_section = document.querySelector("#mrts");
let bottom = document.querySelector("#bottom");
let nextPage = null;
let name;
let data;
let mrt;
let category;
let image;
let target = "/api/attractions?";

// 驗證登入狀態 api/user/auth
userAuth();

function create_attraction_box() {
  let div_attraction = document.createElement("div");
  let a_attraction = document.createElement("a");
  let div_photo = document.createElement("div");
  let div_name_box = document.createElement("div");
  let p_name = document.createElement("p");
  let div_mrt_cat_box = document.createElement("div");
  let div_mrt_box = document.createElement("div");
  let p_mrt = document.createElement("p");
  let div_cat_box = document.createElement("div");
  let p_cat = document.createElement("p");
  div_attraction.className = "attraction";
  a_attraction.href = `/attraction/${data[i]["id"]}`;
  div_photo.className = "photo";
  div_photo.style.backgroundImage = `url('${image}')`;
  div_name_box.className = "name_box";
  p_name.className = "name";
  p_name.innerText = `${name}`;
  div_mrt_cat_box.className = "mrt_cat_box";
  div_mrt_box.className = "mrt_box";
  p_mrt.className = "mrt";
  p_mrt.innerText = `${mrt}`;
  div_cat_box.className = "cat_box";
  p_cat.className = "cat";
  p_cat.innerText = `${category}`;
  attractions.appendChild(div_attraction);
  div_attraction.appendChild(a_attraction);
  a_attraction.appendChild(div_photo);
  a_attraction.appendChild(div_mrt_cat_box);
  div_photo.appendChild(div_name_box);
  div_name_box.appendChild(p_name);
  div_mrt_cat_box.appendChild(div_mrt_box);
  div_mrt_cat_box.appendChild(div_cat_box);
  div_mrt_box.appendChild(p_mrt);
  div_cat_box.appendChild(p_cat);
}

// 開啟頁面，讀取第一頁(page = 0 & no keyword)
let get_attracitons = async () => {
  let resopnse = await fetch("/api/attractions");
  let result = await resopnse.json();
  data = result["data"];
  nextPage = result["nextPage"];
  for (i = 0; i < data.length; i++) {
    name = data[i]["name"];
    mrt = data[i]["mrt"];
    category = data[i]["category"];
    image = data[i]["images"][0];
    create_attraction_box();
  }
};
get_attracitons();

// 滑到底部，讀取下一頁(next page)
const intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  const load_nextPage = async () => {
    if (nextPage != null) {
      bottom.style.display = "none";
      let resopnse = await fetch(`${target}page=${nextPage}`);
      let result = await resopnse.json();
      data = result["data"];
      nextPage = result["nextPage"];
      for (i = 0; i < data.length; i++) {
        name = data[i]["name"];
        mrt = data[i]["mrt"];
        category = data[i]["category"];
        image = data[i]["images"][0];
        create_attraction_box();
      }
    }
  };
  const show_bottom = async () => {
    await load_nextPage();
    if (nextPage != null) {
      bottom.style.display = "block";
    }
  };
  show_bottom();
});
intersectionObserver.observe(bottom);

// 景點搜尋功能
btn.addEventListener("click", async () => {
  let resopnse = await fetch(`/api/attractions?keyword=${filter.value}`);
  let result = await resopnse.json();
  data = result["data"];
  nextPage = result["nextPage"];
  if (data.length == 0) {
    attractions.innerHTML = "<p>無相關資料，請重新搜尋。</p>";
  } else {
    attractions.innerHTML = "";
    target = `/api/attractions?keyword=${filter.value}&`;
    for (i = 0; i < data.length; i++) {
      name = data[i]["name"];
      mrt = data[i]["mrt"];
      category = data[i]["category"];
      image = data[i]["images"][0];
      create_attraction_box();
    }
  }
});
btn.addEventListener("mousedown", () => {
  btn.style.backgroundColor = "rgb(35, 71, 80)";
});
btn.addEventListener("mouseup", () => {
  btn.style.backgroundColor = "rgba(68, 136, 153, 1)";
});

// mrt
const get_mrts = async () => {
  let resopnse = await fetch("/api/mrts");
  let result = await resopnse.json();
  let data = result["data"];
  for (i = 0; i < data.length; i++) {
    let mrt_name = data[i];
    mrt_section.innerHTML += `<div class="mrt">${mrt_name}</div>`;
  }
};

const select_mrt_element = async () => {
  await get_mrts();
  let mrt_element = document.querySelectorAll(".mrt");
  mrt_element.forEach((m) => {
    m.addEventListener("click", async () => {
      filter.value = m.innerText;
      let resopnse = await fetch(`/api/attractions?keyword=${filter.value}`);
      let result = await resopnse.json();
      data = result["data"];
      nextPage = result["nextPage"];
      if (data.length == 0) {
        attractions.innerHTML = "<p>無相關資料，請重新搜尋。</p>";
      } else {
        attractions.innerHTML = "";
        target = `/api/attractions?keyword=${filter.value}&`;
        for (i = 0; i < data.length; i++) {
          name = data[i]["name"];
          mrt = data[i]["mrt"];
          category = data[i]["category"];
          image = data[i]["images"][0];
          create_attraction_box();
        }
      }
    });
  });
};
select_mrt_element();

// mrt_scrolling
left_btn.addEventListener("click", () => {
  mrt_section.scrollLeft -= 500;
});
right_btn.addEventListener("click", () => {
  mrt_section.scrollLeft += 500;
});
left_btn.addEventListener("mouseenter", () => {
  left_btn.src = "/static/images/icon/States=Hovered_left.png";
});
left_btn.addEventListener("mouseleave", () => {
  left_btn.src = "/static/images/icon/States=Default_left.png";
});
right_btn.addEventListener("mouseenter", () => {
  right_btn.src = "/static/images/icon/States=Hovered_right.png";
});
right_btn.addEventListener("mouseleave", () => {
  right_btn.src = "/static/images/icon/States=Default_right.png";
});
