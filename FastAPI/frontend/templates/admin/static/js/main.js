const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
const time = $(".time");
const sub1 = $("#sub1");
const sub12 = $("#sub12");
const sttConnection = $(".statusConnection");
const login = $("#login-btn");
const home = $(".row");
const homePage = $("#home");
const loginForm = $(".main-login");
const logined = $("#user");
const profile = $("#profile-tab");
const boxContent = $(".boxContent");
const homeTab = $("#home-tab");

homeTab.onclick = () => {
  boxContent.style.display = "block";
};
profile.onclick = () => {
  boxContent.style.display = "none";
  console.log(boxContent);
};

// WebSocket
// const ws = new WebSocket("ws://192.168.10.150:8000/ws");
// ws.onmessage = function (event) {
//   const data = JSON.parse(event.data);
//   const template = data.cpu.Temperatue_CPU
//   time.innerHTML = template
//   console.log(template);
// };

