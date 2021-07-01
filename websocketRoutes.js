const websocket = require("ws");
const Messages = require('./public/js/ws_protocol')

const wss = new websocket.Server({ port: 3000 });

wss.on("connection", (ws, req) => {
    let token = req.headers.cookie.split(';').find(cookie => cookie.trim().startsWith('sy_client_token=')).slice(17);
    ws.id = token;
    console.log(`ws-connected: ${token}`);
    ws.on("message", msgStr => {
        console.log(msgStr);
        let msg = JSON.parse(msgStr);
        let data = msg.data;
        switch (data.type) {
            // TODO ws messsage handling
            case Messages.CONNECTED.type:
                break;
        }
    });
});

module.exports = wss;