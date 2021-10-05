import { colorGrads, grad } from "./constants.js";
import { copyToClipboard } from "./utils.js";
import anime from "./anime.es.js"

const players = [];
const los = [];
let available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];


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
        if (los.includes(tokens[1]))
            los.splice(los.findIndex(p => p === tokens[1]), 1);
    } else if (key === "SET_MRX") {
        let oldX = players.findIndex(player => player.color === 'X');
        let newX = players.findIndex(player => player.player_id === tokens[1]);
        console.log(oldX);
        if (oldX !== -1)
            players[oldX].color = players[newX].color;
        players[newX].color = 'X';
    } else if (key === "SET_COLOR") {
        let p = players.findIndex(player => player.player_id === tokens[1]);
        players[p].color = tokens[2];
    } else if (key === "STARTGAME") {
        console.log("starting game"); // TODO do this better
        window.location.assign("/game");
    } else if (key === "LOS") {
        if (!los.includes(tokens[1]))
            los.push(tokens[1]);
    } else if (key === "DISCONNECT") {
        players.splice(players.findIndex(p => p.player_id === tokens[1]), 1);
        if (tokens[[1]] === player_id)
            window.location.assign("/");
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
    document.body.classList.add("los");
    document.getElementById("players").innerHTML = "";
    setTimeout(() => window.location.assign("/"), 500);
}

function updateUI() {
    players.sort((a, b) => a.player_id === player_id ? -1 : b.player_id === player_id ? 1 : 0);
    const self = players[0];
    color = self.color;

    let avail_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];

    let html = "";
    players.forEach(player => {
        html +=
            `<div class="row">
                <div class="col player${los.includes(player.player_id) ? " los" : ""}" id="p-${player.player_id}" style="--bg-color: rgb(var(--color-${player.color}))">
                    <div class="p-info">
                        <span class="material-icons">${player.color === 'X' ? "help_outline" : "person"}</span> 
                        ${player.name} ${player.player_id === player_id ? '(You)' : ''}
                    </div>
                    <div class="reqm" id="b-${player.player_id}"></div>
                </div>
            </div>`;
        let i = avail_colors.findIndex(c => c === player.color);
        if (i !== -1)
            avail_colors.splice(i, 1);
    });
    available_colors = avail_colors;
    document.getElementById("players").innerHTML = html;

    if (isHost)
        players.forEach(player => {
            if (player.color == 'X')
                return;
            let btn = document.createElement("button");
            btn.addEventListener("click", () => reqMrX(player.player_id));
            btn.className = "btn btn-warning reqm";
            btn.innerText = "Set Mr. X";
            btn.style.position = "relative";
            if (los.includes(player.player_id))
                btn.disabled = true;
            document.getElementById("b-" + player.player_id).appendChild(btn);
        });

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

    if (players.length === 6 && isHost) {
        document.getElementById("start").style.display = "initial";
    }

    // color UI
    document.getElementById("colorButton").style.backgroundColor = `rgb(var(--color-${self.color}))`
    if (self.color === 'X') {
        document.getElementById("colorButton").style.display = "none";
    }
    else {
        document.getElementById("colorButton").style.display = "initial";
    }
    let colorListElements = document.getElementById("colorList").children;
    for (let i = 0; i < colorListElements.length; i++) {
        const element = colorListElements[i];
        const c = element.getAttribute("set-col");

        function colorHandler() {
            drawPreview(c);
            reqColor(c);
        }
        console.log(available_colors.includes(c));
        if (c === color) {
            element.style.backgroundColor = `rgba(var(--color-${c}), 0.3)`;
        } else if (!available_colors.includes(c)) {
            element.style.backgroundColor = "#8b8b8b";
            element.removeEventListener("click", colorHandler);
        } else {
            element.style.backgroundColor = "";
            element.addEventListener("click", colorHandler);
        }
    }
}

function drawPreview(c) {
    document.getElementById("playerbody").style.stroke = `rgb(var(--color-${c}))`;

    anime({
        targets: '#playerbody path',
        strokeDashoffset: [anime.setDashoffset, 0],
        easing: 'easeInOutSine',
        delay: function (el, i, n) { return (n - i - 1) * 300 },
        duration: 1000
    });
}

function copyInvite() {
    copyToClipboard(document.getElementById('link'));
    console.log("copied");
}

window.s = socket;

document.getElementById("copy-link").addEventListener("click", copyInvite);
document.getElementById("leave").addEventListener("click", leave);
document.getElementById("start").addEventListener("click", start);
document.getElementById("colorButton").addEventListener("click", () => drawPreview(color));
window.sc = reqColor
window.sm = reqMrX