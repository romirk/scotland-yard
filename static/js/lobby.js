import { colorGrads, gradient, PLAYER_COLORS } from "./constants.js";
import {
  copyToClipboard,
  overlay,
  circlePath,
  linear_gradient,
  cancelAnimation,
  cancelAllAnimations,
} from "./utils.js";
import anime from "./anime.es.js";

/**
 * @typedef {Object} Player
 * @property {string} game_id
 * @property {string} player_id
 * @property {string} names
 * @property {string} color
 * @property {bool} is_host
 * @property {string} state
 */

/**
 * Main lobby app
 * @param {WebSocket} socket
 * @param {Player} player_info
 */
const app = (socket, player_info) => {
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

  const layout = document.getElementById("layout");
  let loop_animation = anime();

  function getPlayerById(id) {
    return players.find((p) => p.player_id === id);
  }

  function getPlayerindex(id) {
    return players.findIndex((player) => player.player_id === id);
  }

  function unload(callback) {
    cancelAllAnimations();
    $("#main").fadeOut(1000);
    console.log("unload");
    linear_gradient(
      gradient,
      { start: "#000", end: "#000", deg: 0 },
      1000,
      layout,
      callback
    );
  }

  // UI
  function updateUI() {
    players.sort(
      (a, b) =>
        (b.player_id === player_info.player_id) -
        (a.player_id === player_info.player_id)
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
    for (const player of players) {
      html += `<div class="row">
                <div class="col player ${player.state}" 
                id="p-${player.player_id}" 
                style="--bg-color: rgb(var(--color-${player.color}))">
                    <div class="p-info">
                        <span class="material-icons">${
                          player.color === "X" ? "help_outline" : "person"
                        }</span> 
                        ${player.name}
                        ${
                          player.player_id === player_info.player_id
                            ? "(You)"
                            : ""
                        }
                    </div>
                    <div class="reqm" id="b-${player.player_id}"></div>
                </div>
            </div>`;
      if (player.state === "new") player.state = "";
      let idx = avail_colors.findIndex((c) => c === player.color);
      if (idx !== -1) avail_colors.splice(idx, 1);
    }
    available_colors = avail_colors;
    document.getElementById("players").innerHTML = html;

    if (player_info.is_host)
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

    console.log(anime.running);
    if (player_info.color !== "X") {
      loop_animation.pause();
      linear_gradient(
        gradient,
        {
          start: "rgb(0, 0, 0)",
          end: `rgba(${colorGrads[player_info.color][0]}, ${
            colorGrads[player_info.color][1]
          }, ${colorGrads[player_info.color][2]}, 1)`,
          deg: 45,
        },
        1000,
        layout
      );
    } else {
      cancelAnimation(loop_animation);
      anime({
        targets: gradient,
        start: "#f00",
        end: "#002aff",
        deg: 135,
        loop: false,
        duration: 3000,
        direction: "normal",
        easing: "easeInOutSine",
        update: () =>
          (layout.style.background = `linear-gradient(${gradient.deg}deg, ${gradient.start}, #000, ${gradient.end}) center / cover`),
      }).finished.then(() => {
        loop_animation = anime({
          targets: gradient,
          deg: () => 100,
          duration: 7000,
          easing: "easeInOutSine",
          direction: "alternate",
          loop: false,
          update: (a) =>
            (layout.style.background = `linear-gradient(${gradient.deg}deg, ${gradient.start}, #000, ${gradient.end}) center / cover`),
        });
      });
    }

    if (players.length === 6 && player_info.is_host) {
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
      console.log(c);
      reqColor(c);
      drawPreview(c);
    };
  }

  function updateColorUI() {
    const colorBtn = document.getElementById("colorButton");
    colorBtn.style.backgroundColor = `rgb(var(--color-${player_info.color}))`;
    if (player_info.color === "X") {
      colorBtn.style.display = "none";
    } else {
      colorBtn.style.display = "block";
    }

    const list = document.getElementById("colorList");
    list.innerHTML = "";
    for (const c of PLAYER_COLORS) {
      const a = document.createElement("a");
      a.className = "list-group-item list-group-item-action";
      a.style.color = `rgb(var(--color-${c}))`;
      a.style.cursor = "default";
      a.innerText = c;

      if (c === player_info.color) {
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

  socket.onclose = (e) => {
    console.log("Socket closed with code: " + e.code);
    if (e.code !== 1000)
      unload(() => window.location.assign("/error/connection%20lost"));
  };

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

      case "PLAYER_JOINED":
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
        player_info.is_host = player_info.player_id === tokens[1];
        getPlayerById(player_info.player_id).is_host = player_info.is_host;
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
        unload(() => {
          console.log("[ws/server]", "unloading");
          socket.close(1000, "Game Started");
          window.location.assign("/");
        });
        break;

      case "LOS":
        players[getPlayerindex(tokens[1])].state = "los";
        break;

      case "DISCONNECT":
        players[getPlayerindex(tokens[1])].state = "disconnect";
        if (tokens[1] === player_info.player_id) window.location.assign("/");
        break;

      case "ERROR":
        window.location.assign(
          "/error/" + encodeURIComponent(msg.data.substring(5))
        );
        break;

      case "ABORT":
        window.location.assign("/error/" + encodeURIComponent("Game aborted"));
        break;

      default:
        return;
    }

    const self = players.find((p) => p.player_id === player_info.player_id);
    if (self) player_info.color = self.color;
    updateUI();
    for (let i = players.length - 1; i >= 0; i--) {
      if (players[i].state === "disconnect") {
        players.splice(i, 1);
      }
    }
  };

  //add data
  document.getElementById("link").innerHTML =
    location.protocol + "//" + window.location.host + "/" + player_info.game_id;

  const heads = document.getElementsByClassName("playerheadpath");
  for (const head of heads) {
    head.setAttribute("d", circlePath(25, 30, 18));
  }

  // event handlers

  function reqColor(c) {
    socket.send(`REQCOLOR ${c}`);
  }

  function reqMrX(pid) {
    if (!player_info.is_host) return;
    socket.send(`REQMRX ${pid}`);
  }

  function startGame() {
    if (!player_info.is_host || players.length !== 6) return;
    socket.send(`READY`);
  }

  function leave() {
    unload(() => {
      socket.send(`LEAVE`);
      socket.close(1000, "Leaving");

      window.location.assign("/");
    });
  }

  // event listeners

  document
    .getElementById("copy-link")
    .addEventListener("click", () =>
      copyToClipboard(document.getElementById("link"))
    );
  document.getElementById("leave_button").addEventListener("click", leave);
  document.getElementById("start").addEventListener("click", startGame);
  document
    .getElementById("colorButton")
    .addEventListener("click", () => drawPreview(player_info.color));
};

$(document).ready(() => {
  $.getJSON("/info", (data) => {
    const player_info = data;
    window.GAME_ID = player_info.game_id;
    const ws_url = `${location.protocol === "https:" ? "wss" : "ws"}://${
      window.location.host
    }/ws/lobby/${player_info.game_id}/${player_info.player_id}`;
    player_info.state = "new";
    const socket = new WebSocket(ws_url);
    app(socket, player_info);
    $("#preload").fadeOut(1200, () => $("#preload").remove());
  });
});
