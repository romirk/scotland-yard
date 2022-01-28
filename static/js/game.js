let move_order = [];
let turn = 0;

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
  wsSend("GET_PLAYER_INFO");
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

  //TODO Handle messages

  let tokens = msg.data.split(" ");
  let command = tokens[0];
  console.log(command);
  switch (command) {
    case "PLAYER_MOVED":
      turn = (turn + 1) % 6;
      if (move_order[turn] == PLAYER_ID) {
        log += "<br><span class=turn>It's your turn!</span>";
      }
      break;

    case "GAME_INFO":
      let gameInfo = JSON.parse(msg.data.split("GAME_INFO ")[1]);
      console.log(gameInfo);
      move_order = gameInfo.move_order;
      break;

    case "GAME_STARTING":
      wsSend("GET_GAME_INFO");
      break;
    default:
      break;
  }
  logElement.innerHTML = log;
};
