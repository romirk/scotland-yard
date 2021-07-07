(function(exports) {

    /**
     * client to server: connect and join game
     * @typedef {Object} CONNECTED
     * 
     */
    exports.CONNECT = {
        type: "CONNECT_LOBBY",
        data: {
            player_id: null,
            name: null,
            color: null,
            isMrX: null
        }
    };

    exports.ACKNOWLEDGE = {
        type: "ACKNOWLEDGE",
        data: {
            game_id: null,
            players: []
        }
    }

    /**
     * server to client
     */
    exports.PLAYER_CONNECTED = {
        type: "PLAYER_CONNECTED",
        data: {
            game_id: null,
            player_id: null,
            name: null,
            color: null,
            isMrX: null
        }
    }

})(typeof exports === "undefined" ? (this.LobbyMessages = {}) : exports);
//if exports is undefined, we are on the client; else the server