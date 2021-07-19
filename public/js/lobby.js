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
    if (data.player_id === player_id) return;
    else players.push(data.name);
    updateList();
});
function updateList() {
    let html = "";
    players.forEach(player => {
        html += "<li><span class=\"material-icons-outlined\">" + (isMrX ? "help_outline": "person") + "</span>" + player + "</li>\n";
    });
    document.getElementById("players").innerHTML = html;

}