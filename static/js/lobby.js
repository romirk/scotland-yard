import { colorGrads, grad } from "./constants.js";
import { copyToClipboard, overlay, circlePath } from "./utils.js";
import anime from "./anime.es.js";

/**
 * @typedef {Object} Player
 * @property {string} player_id
 * @property {string} name
 * @property {string} color
 * @property {bool} is_host
 * @property {string} state
 */

/**
 * Main lobby app
 * @param {WebSocket} socket
 */
const app = (socket) => {
  const my = {
    game_id: GAME_ID,
    player_id: PLAYER_ID,
    name: NAME,
    color: color,
    host_authorization: IS_HOST,
  };

  /** @type {Player[]} */
  const players = [];
  /** @type {Player[]} */
  let available_colors = [
    "red",
    "blue",
    "purple",
    "green",
    "yellow",
    "orange",
    "X",
  ];

  function getPlayerById(id) {
    return players.find((p) => p.player_id === id);
  }

  function getPlayerindex(id) {
    return players.findIndex((player) => player.player_id === id);
  }

  function reqColor(c) {
    socket.send(`REQCOLOR ${c}`);
  }

  function reqMrX(pid) {
    if (!my.host_authorization) return;
    socket.send(`REQMRX ${pid}`);
  }

  function startGame() {
    if (!my.host_authorization || players.length !== 6) return;
    socket.send(`READY`);
  }

  function leave() {
    socket.send(`LEAVE`);
    document.body.classList.add("los");
    document.getElementById("players").innerHTML = "";
    setTimeout(() => window.location.assign("/"), 500);
  }

  // UI
  function updateUI() {
    players.sort((a, b) =>
      a.player_id === my.player_id ? -1 : b.player_id === my.player_id ? 1 : 0
    );

    let avail_colors = [
      "red",
      "blue",
      "purple",
      "green",
      "yellow",
      "orange",
      "X",
    ];

    let html = "";
    let c = 0;
    for (let i = 0; i < players.length; i++) {
      const player = players[i];
      html += `<div class="row">
                <div class="col player ${player.state}" 
                id="p-${player.player_id}" 
                style="--bg-color: rgb(var(--color-${player.color}))">
                    <div class="p-info">
                        <span class="material-icons">${
                          player.color === "X" ? "help_outline" : "person"
                        }</span> 
                        ${player.name}
                        ${player.player_id === my.player_id ? "(You)" : ""}
                    </div>
                    <div class="reqm" id="b-${player.player_id}"></div>
                </div>
            </div>`;
      if (player.state === "new") players[i].state = "";
      let idx = avail_colors.findIndex((c) => c === player.color);
      if (idx !== -1) avail_colors.splice(idx, 1);
    }
    available_colors = avail_colors;
    document.getElementById("players").innerHTML = html;

    if (my.host_authorization)
      players.forEach((player) => {
        if (player.color == "X") return;
        let btn = document.createElement("button");
        btn.addEventListener("click", () => reqMrX(player.player_id));
        btn.className = "btn btn-warning reqm";
        btn.innerText = "Set Mr. X";
        btn.style.position = "relative";
        if (player.state === "los") btn.disabled = true;
        document.getElementById("b-" + player.player_id).appendChild(btn);
      });

    const layout = document.getElementById("layout");

    anime({
      targets: grad,
      c1r: 0,
      c1g: 0,
      c1b: 0,
      c2r: colorGrads[my.color][0],
      c2g: colorGrads[my.color][1],
      c2b: colorGrads[my.color][2],
      duration: 1000,
      easing: "easeInQuad",
      update: () =>
        (layout.style.background = `linear-gradient(45deg, rgb(${grad.c1r}, ${grad.c1g}, ${grad.c1b}), rgb(${grad.c2r}, ${grad.c2g}, ${grad.c2b})) center / cover`),
    });

    if (players.length === 6 && my.host_authorization) {
      document.getElementById("start").style.display = "initial";
    }

    const disconnected_players = document.querySelector(".disconnect");

    if (disconnected_players)
      disconnected_players.addEventListener("animationend", (e) => {
        e.target.parentNode.parentNode.removeChild(e.target.parentNode);
      });
    // color UI
    updateColorUI();
  }

  function colorHandler(c, e) {
    return () => {
      drawPreview(c);
      reqColor(c);
    };
  }

  function updateColorUI() {
    const colorBtn = document.getElementById("colorButton");
    colorBtn.style.backgroundColor = `rgb(var(--color-${my.color}))`;
    if (my.color === "X") {
      colorBtn.style.display = "none";
    } else {
      colorBtn.style.display = "block";
    }

    const list = document.getElementById("colorList");
    list.innerHTML = "";
    for (let i = 0; i < COLORS.length; i++) {
      const c = COLORS[i];

      const a = document.createElement("a");
      a.className = "list-group-item list-group-item-action";
      a.style.color = `rgb(var(--color-${c}))`;
      a.style.cursor = "default";
      a.innerText = c;

      if (c === my.color) {
        a.style.backgroundColor = `rgba(var(--color-${c}), 0.3)`;
      } else if (!available_colors.includes(c)) {
        a.style.color = "#8b8b8b";
        a.style.backgroundColor = "rgb(221,221,221)";
      } else {
        a.style.backgroundColor = "";
        let handler = colorHandler(c);
        a.addEventListener("click", handler, { capture: true, once: true });
        a.classList.add("clickable");
        a.style.cursor = "pointer";
      }
      list.appendChild(a);
    }
  }

  function drawPreview(c) {
    console.log("draw");
    document.getElementById(
      "playerbody"
    ).style.stroke = `rgb(var(--color-${c}))`;

    anime({
      targets: "#playerbody path",
      strokeDashoffset: [anime.setDashoffset, 0],
      easing: "easeInOutSine",
      delay: function (el, i, n) {
        return (n - i - 1) * 300;
      },
      duration: 1000,
    });
  }

  // sockets

  socket.onclose = () => window.location.assign("/");
  socket.onopen = () => socket.send("JOIN " + my.player_id);

  socket.onmessage = (msg) => {
    console.log("[ws/server]", msg.data);
    let tokens = msg.data.split(" ");
    let key = tokens[0];
    const player_ids = players.map((e) => e.player_id);

    switch (key) {
      case "ACKNOWLEDGE":
        let playerdata = msg.data.split("\n").slice(1);
        if (parseInt(tokens[1]) !== 0)
          playerdata.forEach((playerstr) => {
            let info = playerstr.split(" ");
            players.push({
              player_id: info[0],
              name: info[1],
              color: info[2],
              is_host: info[3],
              state: "new",
            });
          });
        document.getElementById("main").style.display = "block";
        document.getElementById("copy-link").style.display = "initial";
        break;

      case "NEW_PLAYER":
        if (!player_ids.includes(tokens[1]))
          players.push({
            player_id: tokens[1],
            name: tokens[2],
            color: tokens[3],
            is_host: tokens[4],
            state: "new",
          });
        else if (getPlayerById(tokens[1]).state === "los")
          players[getPlayerindex(tokens[1])].state = "";
        break;

      case "SET_HOST":
        my.host_authorization = my.player_id === tokens[1];
        getPlayerById(my.player_id).is_host = my.host_authorization;
        break;

      case "SET_MRX":
        let oldX = players.findIndex((player) => player.color === "X");
        let newX = getPlayerindex(tokens[1]);
        if (oldX !== -1) players[oldX].color = players[newX].color;
        players[newX].color = "X";
        break;

      case "SET_COLOR":
        let p = getPlayerindex(tokens[1]);
        players[p].color = tokens[2];
        break;

      case "STARTGAME":
        overlay.on();
        setTimeout(() => window.location.assign("/game"), 1000);
        break;

      case "LOS":
        players[getPlayerindex(tokens[1])].state = "los";
        break;

      case "DISCONNECT":
        players[getPlayerindex(tokens[1])].state = "disconnect";
        if (tokens[1] === my.player_id) window.location.assign("/");
        break;

      case "ERROR":
        window.location.assign(
          "/error/" + encodeURIComponent(msg.data.substring(5))
        );
        break;

      default:
        return;
    }

    const self = players.find((p) => p.player_id === my.player_id);
    if (self) my.color = self.color;
    updateUI();
    for (let i = players.length - 1; i >= 0; i--) {
      if (players[i].state === "disconnect") {
        players.splice(i, 1);
      }
    }
  };

  //add data
  document.getElementById("link").innerHTML =
    location.protocol + "//" + window.location.host + "/" + my.game_id;

  const heads = document.getElementsByClassName("playerheadpath");
  for (let i = 0; i < heads.length; i++) {
    heads[i].setAttribute("d", circlePath(25, 30, 18));
  }

  // event listeners

  document
    .getElementById("copy-link")
    .addEventListener("click", () =>
      copyToClipboard(document.getElementById("link"))
    );
  document.getElementById("leave").addEventListener("click", leave);
  document.getElementById("start").addEventListener("click", startGame);
  document
    .getElementById("colorButton")
    .addEventListener("click", () => drawPreview(my.color));
};

window.addEventListener("load", () => {
  console.log("start");

  const socket = new WebSocket(
    `ws${location.protocol === "https:" ? "s" : ""}://${
      window.location.host
    }/ws/lobby/${GAME_ID}`
  );

  app(socket);
});
