let attractions = document.querySelector("#attractions");
let filter = document.querySelector("#attraction_filter");
let btn = document.querySelector("#search_btn");
let left_btn = document.querySelector("#left");
let right_btn = document.querySelector("#right");
let mrt_section = document.querySelector("#mrts");
let bottom = document.querySelector("#bottom");
let nextPage = null;
let target = "/api/attractions?";

// 開啟頁面，讀取第一頁(page = 0 & no keyword)
let get_attracitons = async () => {
  let resopnse = await fetch("/api/attractions");
  let result = await resopnse.json();
  let data = result["data"];
  nextPage = result["nextPage"];
  for (i = 0; i < data.length; i++) {
    let name = data[i]["name"];
    let mrt = data[i]["mrt"];
    let category = data[i]["category"];
    let image = data[i]["images"][0];
    attractions.innerHTML += `<div class='attraction'><a href='/attraction/${data[i]["id"]}'><div class='photo' style="background-image: url('${image}');"><div class='name_box'><p class='name'>${name}</p></div></div><div class='mrt_cat_box'><div class='mrt_box'><p class='mrt'>${mrt}</p></div><div class='cat_box'><p class='cat'>${category}</p></div></div></a></div>`;
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
      let data = result["data"];
      nextPage = result["nextPage"];
      for (i = 0; i < data.length; i++) {
        let name = data[i]["name"];
        let mrt = data[i]["mrt"];
        let category = data[i]["category"];
        let image = data[i]["images"][0];
        attractions.innerHTML += `<div class='attraction'><a href='/attraction/${data[i]["id"]}'><div class='photo' style="background-image: url('${image}');"><div class='name_box'><p class='name'>${name}</p></div></div><div class='mrt_cat_box'><div class='mrt_box'><p class='mrt'>${mrt}</p></div><div class='cat_box'><p class='cat'>${category}</p></div></div></a></div>`;
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
  let data = result["data"];
  nextPage = result["nextPage"];
  if (data.length == 0) {
    attractions.innerHTML = "<p>無相關資料，請重新搜尋。</p>";
  } else {
    attractions.innerHTML = "";
    target = `/api/attractions?keyword=${filter.value}&`;
    for (i = 0; i < data.length; i++) {
      let name = data[i]["name"];
      let mrt = data[i]["mrt"];
      let category = data[i]["category"];
      let image = data[i]["images"][0];
      attractions.innerHTML += `<div class='attraction'><a href='/attraction/${data[i]["id"]}'><div class='photo' style="background-image: url('${image}');"><div class='name_box'><p class='name'>${name}</p></div></div><div class='mrt_cat_box'><div class='mrt_box'><p class='mrt'>${mrt}</p></div><div class='cat_box'><p class='cat'>${category}</p></div></div></a></div>`;
    }
  }
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
  mrt_element.forEach((mrt) => {
    mrt.addEventListener("click", async () => {
      filter.value = mrt.innerHTML;
      let resopnse = await fetch(`/api/attractions?keyword=${mrt.innerHTML}`);
      let result = await resopnse.json();
      let data = result["data"];
      nextPage = result["nextPage"];
      if (data.length == 0) {
        attractions.innerHTML = "<p>無相關資料，請重新搜尋。</p>";
      } else {
        attractions.innerHTML = "";
        target = `/api/attractions?keyword=${mrt.innerHTML}&`;
        for (i = 0; i < data.length; i++) {
          let name = data[i]["name"];
          let mrt = data[i]["mrt"];
          let category = data[i]["category"];
          let image = data[i]["images"][0];
          attractions.innerHTML += `<div class='attraction'><a href='/attraction/${data[i]["id"]}'><div class='photo' style="background-image: url('${image}');"><div class='name_box'><p class='name'>${name}</p></div></div><div class='mrt_cat_box'><div class='mrt_box'><p class='mrt'>${mrt}</p></div><div class='cat_box'><p class='cat'>${category}</p></div></div></a></div>`;
        }
      }
    });
  });
};
select_mrt_element();

// mrt_scrolling
left_btn.addEventListener("click", () => {
  mrt_section.scrollLeft -= 600;
});
right_btn.addEventListener("click", () => {
  mrt_section.scrollLeft += 600;
});
