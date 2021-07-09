const GameMessages = require('./public/js/ws_protocol');
const LobbyMessages = require('./public/js/ws_lobby_protocol');
const multiplayer = require('./multiplayerHandler');

function createRoutes(io) {
    // TODO handle ws connections
    io.on('connection', socket => {
        socket.on(LobbyMessages.CONNECT.type, msg => {
            let data = JSON.parse(msg).data;
            console.log(`ws-lobby-connected: ${data}`);
            
            let ackObj = LobbyMessages.ACKNOWLEDGE;
            let game_id = ackObj.data.game_id = multiplayer.getGameWithPlayer(data.player_id);
            ackObj.data.players = multiplayer.getAllPlayersInGame(game_id);
            socket.join(game_id);
            socket.emit(LobbyMessages.ACKNOWLEDGE.type, JSON.stringify(ackObj));

            let plrConObj = LobbyMessages.PLAYER_CONNECTED;
            plrConObj.data = data;
            plrConObj.data.game_id = game_id;
            io.to(game_id).emit(LobbyMessages.PLAYER_CONNECTED.type, JSON.stringify(plrConObj));
        });

        socket.on(GameMessages.MOVE_REQUEST.type, msg => {
            //TODO handle ws move request
            multiplayer.move();
            
        });
    });

    return io;
}

module.exports = createRoutes;