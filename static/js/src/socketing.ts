import Logger from "./logger";

class WsHandler {
    ws: WebSocket;
    constructor(ws: WebSocket, logger: Logger) {
        this.ws = ws;
    }
}