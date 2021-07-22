const LobbyMessages = require('../public/js/ws_lobby_protocol');
const multiplayer = require('../multiplayerHandler');

function createEvents(io, socket) {

    // connect event
    socket.on(LobbyMessages.CONNECT.type, msg => {
        let data = JSON.parse(msg).data;
        console.log(`ws-lobby-connected: ${data}`);
        
        let ackObj = LobbyMessages.ACKNOWLEDGE;
        let game_id = ackObj.data.game_id = multiplayer.getGameByPlayer(data.player_id);
        ackObj.data.players = multiplayer.getAllPlayersInGame(game_id);
        socket.join(game_id);
        socket.emit(LobbyMessages.ACKNOWLEDGE.type, JSON.stringify(ackObj));

        let plrConObj = LobbyMessages.PLAYER_CONNECTED;
        plrConObj.data = data;
        plrConObj.data.game_id = game_id;
        io.to(game_id).emit(LobbyMessages.PLAYER_CONNECTED.type, JSON.stringify(plrConObj));
    });

    // request color event
    socket.on(LobbyMessages.REQUEST_COLOR.type, msg => {
        let data = JSON.parse(msg).data;
        let result = multiplayer.setColor(data.game_id, data.player_id, data.color);

        if (result) {
            let setColorObj = LobbyMessages.SET_COLOR;
            setColorObj.data = data;
            io.to(data.game_id).emit(LobbyMessages.SET_COLOR.type, JSON.stringify(setColorObj));
        }
    })

    return socket;
}

module.exports = createEvents;