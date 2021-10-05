import { available_colors, colorGrads, grad } from "./constants.js";
import { copyToClipboard } from "./utils.js";
import anime from "./anime.es.js"

const players = [];

document.getElementById("link").innerHTML = window.location.host + '/' + game_id;

const socket = new WebSocket(`ws${location.protocol === 'https:' ? 's' : ''}://${window.location.host}/ws/lobby/${game_id}`);

socket.onclose = () => window.location.assign("/");
socket.onopen = () => socket.send("JOIN " + player_id);
socket.onclose = () => console.log("socket closed");

socket.onmessage = msg => {
    console.log("[ws/server]", msg.data);
    let tokens = msg.data.split(' ');
    let key = tokens[0];
    if (key === "ACKNOWLEDGE") {
        let playerdata = msg.data.split('\n').slice(1);
        if (parseInt(tokens[1]) !== 0)
            playerdata.forEach(playerstr => {
                let info = playerstr.split(' ');
                players.push({ player_id: info[0], name: info[1], color: info[2] })
            });
    } else if (key === "NEW_PLAYER") {
        if (!players.map(e => e.player_id).includes(tokens[1]))
            players.push({ player_id: tokens[1], name: tokens[2], color: tokens[3] });
        updateAvailableColors(tokens[2]);
    } else if (key === "SET_MRX") {
        let oldX = players.findIndex(player => player.color === 'X');
        let newX = players.findIndex(player => player.player_id === tokens[1]);
        console.log(oldX);
        if (oldX !== -1)
            players[oldX].color = players[newX].color;
        players[newX].color = 'X';
    } else if (key === "SET_COLOR") {
        let p = players.findIndex(player => player.player_id === tokens[1]);
        available_colors.push(players[p].color)
        available_colors.splice(available_colors.findIndex(color => color === tokens[2]), 1);
        players[p].color = tokens[2];
    }
    else if (key === "STARTGAME") {
        console.log("starting game"); // TODO do this better
        window.location.assign("/game");
    } else if (key === "DISCONNECT") {
        players.splice(players.findIndex(p => p.player_id === tokens[1]), 1);
    }
    updateUI();
    console.log(players);
}

function reqColor(color) {
    socket.send(`REQCOLOR ${player_id} ${color}`);
}

function reqMrX(pid) {
    if (!isHost)
        return;
    socket.send(`REQMRX ${player_id} ${pid}`);
}

function start() {
    if (!isHost || players.length !== 6) return;
    socket.send(`READY ${player_id}`);

}

function leave() {
    socket.send(`DISCONNECT ${player_id}`);
    window.location.assign("/");
}

function updateUI() {
    const playersElement = document.getElementById("players");
    let html = "";
    players.forEach(player => {
        html +=
            `<div class="row">\n
                \t<div class="col player" id="p-${player.player_id}"" style="--bg-color: var(--color-${player.color})">\n
                    \t\t<span class="material-icons">${player.color === 'X' ? "help_outline" : "person"}</span> 
                    ${player.name} ${player.player_id === player_id ? '(You)' : ''}\n
                \t</div>\n
            </div>\n`;
    });

    playersElement.innerHTML = html;
    if (isHost)
        players.forEach(player => {
            if (player.color == 'X')
                return;
            let btn = document.createElement("button");
            btn.addEventListener("click", () => reqMrX(player.player_id));
            btn.className = "btn btn-warning reqm";
            btn.innerText = "Set Mr. X";
            document.getElementById("p-" + player.player_id).appendChild(btn);
        });

    const self = players.find(p => p.player_id === player_id);
    const layout = document.getElementById("layout");

    anime({
        targets: grad,
        c1r: 0,
        c1g: 0,
        c1b: 0,
        c2r: colorGrads[self.color][0],
        c2g: colorGrads[self.color][1],
        c2b: colorGrads[self.color][2],
        duration: 1000,
        easing: 'easeInQuad',
        update: () => layout.style.background =
            `linear-gradient(45deg, rgb(${grad.c1r}, ${grad.c1g}, ${grad.c1b}), rgb(${grad.c2r}, ${grad.c2g}, ${grad.c2b})) center / cover`
    });

    if (players.length === 6) {
        document.getElementById("start").style.display = "initial";
    }
    // TODO update color UI

}

function updateAvailableColors(unavailableColor) {
    let index = available_colors.indexOf(unavailableColor);
    if (index !== -1) available_colors.splice(index, 1);
}

function copyInvite() {
    copyToClipboard(document.getElementById('link'));
    console.log("copied");
}

window.s = socket;

document.getElementById("copy-link").addEventListener("click", copyInvite);
document.getElementById("leave").addEventListener("click", leave);
document.getElementById("start").addEventListener("click", start);
document.getElementById("reqc").addEventListener("click", reqColor);
window.sc = reqColor
window.sm = reqMrX