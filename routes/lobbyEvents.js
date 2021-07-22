const LobbyMessages = require('../public/js/ws_lobby_protocol');
const multiplayer = require('../multiplayerHandler');

function createEvents(io, socket) {

    // connect event
    socket.on(LobbyMessages.CONNECT.type, msg => {
        
        let data = JSON.parse(msg).data;
        console.log(`ws-lobby-connected: ${data.player_id}`);
        socket.player_id = data.player_id;
        let ackObj = LobbyMessages.ACKNOWLEDGE;
        let game_id = ackObj.data.game_id = multiplayer.getGameByPlayer(data.player_id);
        socket.game_id = game_id;
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
        let result = multiplayer.setColor(socket.game_id, socket.player_id, data.color);

        if (result) {
            let setColorObj = LobbyMessages.SET_COLOR;
            setColorObj.data = data;
            io.to(socket.game_id).emit(LobbyMessages.SET_COLOR.type, JSON.stringify(setColorObj));
        }
    });

    //request change of Mr X event
    socket.on(LobbyMessages.REQUEST_MRX.type, msg =>{
        let data = JSON.parse(msg).data;
        let newXId = data.player_id;
        multiplayer.setMrX(socket.game_id, newXId);
        let setMrXObj = LobbyMessages.SET_MRX;
        setMrXObj.data.player_id = newXId;
        io.to(socket.game_id).emit(LobbyMessages.SET_MRX.type, JSON.stringify(setMrXObj));
    })

    // socket.on('disconnect', () => {
    //     let disConObj = LobbyMessages.PLAYER_DISCONNECTED;
    //     multiplayer.disconnect(socket.player_id);
    //     disConObj.data = {game_id: socket.game_id, player_id: socket.player_id};
    //     io.to(socket.game_id).emit(LobbyMessages.PLAYER_DISCONNECTED.type, JSON.stringify(disConObj));
    // });

    return socket;
}

module.exports = createEvents;