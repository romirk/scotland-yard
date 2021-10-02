import {copyToClipboard} from "./utils.js";

const players = [];
const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];
const isHost = player_id === game_id;

document.getElementById("link").innerText = window.location.host + '/' + game_id;

const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/' + game_id);

socket.onmessage = msg => console.log("[ws/server]", msg.data);
socket.onclose = () => console.log("socket closed");
socket.onopen = () => socket.send("JOIN " + player_id);

function setColor(color) {
    let reqColObj = Messages.REQUEST_COLOR;
    reqColObj.data.color = color;
    // socket.emit(Messages.REQUEST_COLOR.type, JSON.stringify(reqColObj));
}

function setMrX(newXId) {
    if (!isHost) return;
    let reqXObj = Messages.REQUEST_MRX;
    reqXObj.data.player_id = newXId;
    // socket.emit(Messages.REQUEST_MRX.type, JSON.stringify(reqXObj));
}


function updateUI() {
    let html = "";
    players.forEach(player => {
        html += `<div class="row">\n
            \t<div class="col player" style="background-color: var(--color-${player.color})">\n
                \t\t<span class="material-icons" style="position: relative; top: 0.5vh">${player.isMrX ? "help_outline" : "person"}</span> 
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
    var e = document.getElementById('link');
    copyToClipboard(e);
    console.log("copied");
}

document.getElementById("copy-link").addEventListener("click", copyInvite)