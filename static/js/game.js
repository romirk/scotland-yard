const socket = new WebSocket(
  `ws${location.protocol === "https:" ? "s" : ""}://${
    window.location.host
  }/ws/game/${GAME_ID}`
);

socket.onclose = function (event) {
  console.log("Socket closed");
  // window.location.assign("/");
};

socket.onopen = function (event) {
  console.log("Socket opened");
  wsSend("JOIN " + PLAYER_ID);
  wsSend("GET_GAME_INFO " + PLAYER_ID);
  wsSend("GET_PLAYER_INFO ALL");
};

const commandbox = document.getElementById("ws-command");
commandbox.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    wsSend(commandbox.innerText);
    commandbox.innerText = "";
  }
});
commandbox.focus(); //autofocus on commandbox

let log = "";
const logElement = document.getElementById("gameLog");

function wsSend(msg) {
  socket.send(msg);
  log += `<br><span style="color:blue">${msg}</span>`;
  logElement.innerHTML = log;
}

// document.getElementById("send").addEventListener("click", () => {
//   wsSend(commandbox.innerText);
// });

socket.onmessage = (msg) => {
  console.log(msg);
  log += "<br>" + msg.data;
  logElement.innerHTML = log;

  //TODO Handle messages
};
