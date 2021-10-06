import { colorGrads, grad } from "./constants.js";
import { copyToClipboard } from "./utils.js";
import anime from "./anime.es.js"

let info;
try {
    info = {
        game_id: GAME_ID,
        player_id: PLAYER_ID,
        name: NAME,
        color: color,
        isHost: IS_HOST
    };
} catch (error) {
    window.location.assign("/");
}

const my = info;

const players = [];
const los = [];
let available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];


document.getElementById("link").innerHTML = location.protocol + "//"+ window.location.host + '/' + my.game_id;

const socket = new WebSocket(`ws${location.protocol === 'https:' ? 's' : ''}://${window.location.host}/ws/lobby/${my.game_id}`);

socket.onclose = () => window.location.assign("/");
socket.onopen = () => socket.send("JOIN " + my.player_id);

socket.onmessage = msg => {
    console.log("[ws/server]", msg.data);
    let tokens = msg.data.split(' ');
    let key = tokens[0];
    if (key === "ACKNOWLEDGE") {
        let playerdata = msg.data.split('\n').slice(1);
        if (parseInt(tokens[1]) !== 0)
            playerdata.forEach(playerstr => {
                let info = playerstr.split(' ');
                players.push({ player_id: info[0], name: info[1], color: info[2], isHost: info[3] });
            });
    } else if (key === "NEW_PLAYER") {
        if (!players.map(e => e.player_id).includes(tokens[1]))
            players.push({ player_id: tokens[1], name: tokens[2], color: tokens[3], isHost: tokens[4] });

        if (los.includes(tokens[1]))
            los.splice(los.findIndex(p => p === tokens[1]), 1);
    } else if (key === "SET_HOST") {
        my.isHost = my.player_id === tokens[1];
        players.find(p => p.player_id === my.player_id).isHost = my.isHost;
    } else if (key === "SET_MRX") {
        let oldX = players.findIndex(player => player.color === 'X');
        let newX = players.findIndex(player => player.player_id === tokens[1]);
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
        if (tokens[1] === my.player_id)
            window.location.assign("/");
    }

    const self = players.find(p => p.player_id === my.player_id)
    my.color = self.color;
    updateUI();
}

function reqColor(c) {
    socket.send(`REQCOLOR ${my.player_id} ${c}`);
}

function reqMrX(pid) {
    if (!my.isHost)
        return;
    socket.send(`REQMRX ${my.player_id} ${pid}`);
}

function start() {
    if (!my.isHost || players.length !== 6) return;
    socket.send(`READY ${my.player_id}`);

}

function leave() {
    socket.send(`DISCONNECT ${my.player_id}`);
    document.body.classList.add("los");
    document.getElementById("players").innerHTML = "";
    setTimeout(() => window.location.assign("/"), 500);
}



function updateUI() {
    players.sort((a, b) => a.player_id === my.player_id ? -1 : b.player_id === my.player_id ? 1 : 0);

    let avail_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];

    let html = "";
    players.forEach(player => {
        html +=
            `<div class="row">
                <div class="col player${los.includes(player.player_id) ? " los" : ""}" id="p-${player.player_id}" style="--bg-color: rgb(var(--color-${player.color}))">
                    <div class="p-info">
                        <span class="material-icons">${player.color === 'X' ? "help_outline" : "person"}</span> 
                        ${player.name} ${player.player_id === my.player_id ? '(You)' : ''}
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

    if (my.isHost)
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
        c2r: colorGrads[my.color][0],
        c2g: colorGrads[my.color][1],
        c2b: colorGrads[my.color][2],
        duration: 1000,
        easing: 'easeInQuad',
        update: () => layout.style.background =
            `linear-gradient(45deg, rgb(${grad.c1r}, ${grad.c1g}, ${grad.c1b}), rgb(${grad.c2r}, ${grad.c2g}, ${grad.c2b})) center / cover`
    });

    if (players.length === 6 && my.isHost) {
        document.getElementById("start").style.display = "initial";
    }

    // color UI
    updateColorUI();
}

function colorHandler(c, e) {
    return () => {
        drawPreview(c);
        reqColor(c);
    }
}

function updateColorUI() {
    const colorBtn = document.getElementById("colorButton");
    colorBtn.style.backgroundColor = `rgb(var(--color-${my.color}))`
    if (my.color === 'X') {
        colorBtn.style.display = "none";
    }
    else {
        colorBtn.style.display = "block";
    }

    const list = document.getElementById("colorList");
    list.innerHTML = "";
    for (let i = 0; i < COLORS.length; i++) {
        const c = COLORS[i];

        const a = document.createElement("a");
        a.className = "list-group-item list-group-item-action";
        a.style.color = `rgb(var(--color-${c}))`
        a.innerText = c;

        if (c === my.color) {
            a.style.backgroundColor = `rgba(var(--color-${c}), 0.3)`;
        } else if (!available_colors.includes(c)) {
            a.style.backgroundColor = "#8b8b8b";
        } else {
            a.style.backgroundColor = "";
            let handler = colorHandler(c);
            a.addEventListener("click", handler, { capture: true });
            a.classList.add("clickable")
        }
        list.appendChild(a);
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

document.getElementById("copy-link").addEventListener("click", () => copyToClipboard(document.getElementById('link')));
document.getElementById("leave").addEventListener("click", leave);
document.getElementById("start").addEventListener("click", start);
document.getElementById("colorButton").addEventListener("click", () => drawPreview(my.color));
