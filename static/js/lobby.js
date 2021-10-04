import { copyToClipboard } from "./utils.js";
import anime from "./anime.es.js"

const players = [];
const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];
const grad = {
    c1r: 109, c1g: 182, c1b: 243,
    c2r: 195, c2g: 208, c2b: 56
}

const colorGrads = {
    "red": [189, 40, 40],
    "purple": [133, 78, 241],
    "blue": [30, 73, 169],
    "green": [83, 169, 30],
    "yellow": [221, 165, 33],
    "orange": [207, 106, 19],
    "X": [255, 255, 255]
};

document.getElementById("link").innerHTML = window.location.host + '/' + game_id;

const socket = new WebSocket(`ws://${window.location.host}/ws/lobby/${game_id}`);

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
    } else if (key === "NEW_PLAYER") {
        if (!players.map(e => e.player_id).includes(tokens[1]))
            players.push({ player_id: tokens[1], name: tokens[2], color: tokens[3] });
        updateAvailableColors(tokens[2]);
    }
    else if (key === "SET_MRX") {
        let oldX = players.findIndex(player => player.color === 'X');
        let newX = players.findIndex(player => player.player_id === tokens[1]);
        players[oldX].color = players[newX.color];
        players[newX].color = 'X';
    }
    else if (key === "SET_COLOR") {
        let p = players.findIndex(player => player.player_id === tokens[1]);
        available_colors.push(players[p].color)
        players[p].color = tokens[2];
    }
    else if (key === "STARTGAME") {
        alert("starting game"); // TODO do this better
        window.location.assign("/game");
    }
    else if (key === "DISCONNECT") {
        players.splice(players.findIndex(p => p.player_id === tokens[1]), 1);
    }
    updateUI();
    console.log(players);
}

function reqColor(color) {
    socket.send(`REQCOLOR ${player_id} ${color}`)
}

function reqMrX() {
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
window.sc = reqColor
window.sm = reqMrX