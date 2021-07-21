const GameMessages = require('../public/js/ws_protocol');
const multiplayer = require('../multiplayerHandler');
const lobbyEvents = require('./lobbyEvents');
const gameEvents = require('./gameEvents');

function createRoutes(io) {
    // TODO handle ws connections
    io.on('connection', socket => {
        socket = lobbyEvents(io, socket);
        socket = gameEvents(io, socket);
    });

    return io;
}

module.exports = createRoutes;