import {copyToClipboard} from "./utils.js";

const players = [];
const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];

document.getElementById("link").innerHTML = window.location.host + '/' + game_id;

const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/' + game_id);

socket.onclose = () => console.log("socket closed");
socket.onopen = () => socket.send("JOIN " + player_id);

socket.onmessage = msg => {
    console.log("[ws/server]", msg.data);
    let tokens = msg.data.split(' ');
    let key = tokens[0];
    if (key === "ACKNOWLEDGE") {
        let playerdata = msg.data.split('\n').slice(1);
        playerdata.forEach(playerstr => {
            let info = playerstr.split(' ');
            players.push({ player_id: info[0], name: info[1], color: info[2] })
        });
    } else if (key === "NEW_PLAYER")
        if (!players.map(e => e.player_id).includes(tokens[1]))
            players.push({ player_id: tokens[1], name: tokens[2], color: tokens[3] });
    updateUI();
    console.log(players);
}

function setColor(color) {
    socket.send(`REQCOLOR ${player_id} ${color}`)
}

function setMrX(newXId) {
    socket.send(`REQMRX ${player_id} ${color}`)
}


function updateUI() {
    let html = "";
    players.forEach(player => {
        html += `<div class="row">\n
            \t<div class="col player" style="background-color: var(--color-${player.color})">\n
                \t\t<span class="material-icons">${player.color === 'X' ? "help_outline" : "person"}</span> 
                ${player.name} ${player.player_id === player_id ? '(You)' : ''}\n
            \t</div>\n
        </div>\n`;
    });
    document.getElementById("players").innerHTML = html;
    // TODO update color UI
}

function updateAvailableColors(unavailableColor) {
    let index = available_colors.indexOf(unavailableColor);
    if (index !== -1) available_colors.splice(index, 1);
}

function copyInvite() {
    const e = document.getElementById('link');
    copyToClipboard(e);
    console.log("copied");
}

document.getElementById("copy-link").addEventListener("click", copyInvite);
window.sc = setColor
window.sm = setMrX