const Messages = require('./public/js/ws_protocol');
const multiplayer = require('./multiplayerHandler');

function createRoutes(io) {
    // TODO handle ws connections
    io.on('connection', socket => {
        socket.on(Messages.CONNECTED.type, msg => {
            let data = JSON.parse(msg).data;
            console.log(`Connected: ${data}`);
            socket.join(data.token);
            let ackObj = Messages.ACKNOWLEDGE;
            ackObj.token = data.token;
            socket.to(socket.id).emit(Messages.ACKNOWLEDGE.type, JSON.stringify(ackObj));
        });
    });

    return io;
}

module.exports = createRoutes;