import { copyToClipboard } from "./utils";

const players = [];
const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];
const isHost = player_id === game_id;

let socket = io();
const Messages = this.LobbyMessages;

$('#link').html(window.location.host + '/' + game_id)

let connectedObj = Messages.CONNECT;
connectedObj.data.player_id = player_id;
connectedObj.data.name = name;
connectedObj.data.color = color;
connectedObj.data.isMrX = isMrX;

socket.emit(Messages.CONNECT.type, JSON.stringify(connectedObj));

socket.on(Messages.ACKNOWLEDGE.type, (msg) => {
    let data = JSON.parse(msg).data;
    console.log("connected to", data.game_id)
    console.log("connected players:", data.players);
    data.players.forEach(player => {
        players.push(player);
        updateAvailableColors(player.color);
    });
    updateUI();
});

socket.on(Messages.PLAYER_CONNECTED.type, msg => {
    let data = JSON.parse(msg).data;
    console.log("player joined: ", data);
    if (data.player_id === player_id || players.map(p => p.player_id).includes(data.player_id));
    else
        players.push(data)
    updateAvailableColors(data.color)
    updateUI();
});

// socket.on(Messages.PLAYER_DISCONNECTED.type, msg => {
//     let data = JSON.parse(msg).data;
//     let i = players.map(player => player.player_id).indexOf(data.player_id);
//     available_colors.push(players[i].color);
//     players.splice(i, 1);
//     updateUI();
// })

socket.on(Messages.SET_COLOR.type, msg => {
    let data = JSON.parse(msg).data;
    let i = players.findIndex(player => player.player_id === data.player_id);
    available_colors.push(players[i].color);
    players[i].color = data.color;
    updateAvailableColors(data.color);
    console.log(`${players[i].name} changed to ${data.color}`);
    updateUI();
});

socket.on(Messages.SET_MRX.type, msg => {
    let data = JSON.parse(msg).data;
    let newXIndex = players.findIndex(player => player.player_id === data.player_id);
    let oldXIndex = players.findIndex(player => player.isMrX === true);
    players[oldXIndex].isMrX = false;
    players[newXIndex].isMrX = true;
    players[oldXIndex].color = players[newXIndex].color;
    players[newXIndex].color = 'X';
    updateUI();
})

function setColor(color) {
    let reqColObj = Messages.REQUEST_COLOR;
    reqColObj.data.color = color;
    socket.emit(Messages.REQUEST_COLOR.type, JSON.stringify(reqColObj));
}

function setMrX(newXId) {
    if(!isHost) return;
    let reqXObj = Messages.REQUEST_MRX;
    reqXObj.data.player_id = newXId;
    socket.emit(Messages.REQUEST_MRX.type, JSON.stringify(reqXObj));
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
}

