const GameMessages = require('../public/js/ws_game_protocol');
const multiplayer = require('../multiplayerHandler');

function createEvents(io, socket) {

    //TODO register game events
    socket.on(GameMessages.MOVE_REQUEST.type, msg => {
        multiplayer.move();
    });

    return socket;
}

module.exports = createEvents;