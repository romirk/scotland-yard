const players = [];
const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];

let socket = io();
const Messages = this.LobbyMessages;

document.getElementById('link').innerText = window.location.host + '/' + game_id;

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
    });            
    updateList();
});
socket.on(Messages.PLAYER_CONNECTED.type, msg => {
    let data = JSON.parse(msg).data;
    console.log("player joined: ", data);
    if (data.player_id === player_id || players.map(p => p.player_id).includes(data.player_id));
    else players.push(data);
    updateList();
});
function updateList() {
    let html = "";
    players.forEach(player => {
        html += `<div class="row"><div class="col player" style="background-color: var(--color-${player.color})"><span class="material-icons" style="position: relative; top: 0.5vh">${player.isMrX ? "help_outline": "person"}</span> ${player.name}</div></div>\n`;
    });
    document.getElementById("players").innerHTML = html;

}