const socket = new WebSocket(
  `ws${location.protocol === "https:" ? "s" : ""}://${
    window.location.host
  }/ws/game/${GAME_ID}`
);

socket.onclose = function (event) {
  console.log("Socket closed");
};

socket.onopen = function (event) {
  console.log("Socket opened");
    wsSend("JOIN " + GAME_ID);
};

const commandbox = document.getElementById("ws-command");
commandbox.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    wsSend(commandbox.value);
  }
});

let log = "";
const logElement = document.getElementById("gameLog");

function wsSend(msg) {
  socket.send(msg);
  log += `<br><span style="color:blue">${msg}</span>`;
  logElement.innerHTML = log;
}

document.getElementById("send").addEventListener("click", () => {
  wsSend(commandbox.value);
});

socket.onmessage = (msg) => {
  console.log(msg);
  log += "<br>" + msg.data;
  logElement.innerHTML = log;
};
