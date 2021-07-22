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

    /**
     * server to client
     */
    exports.PLAYER_DISCONNECTED = {
        type: "PLAYER_DISCONNECTED",
        data: {
            game_id: null,
            player_id: null
        }
    }

    /**
     * client to server
     */
    exports.REQUEST_COLOR = {
        type: "REQUEST_COLOR",
        data: {
            color: null
        }
    }

    /**
     * client to server
     */
     exports.REQUEST_MRX = {
        type: "REQUEST_MRX",
        data: {
            player_id: null
        }
    }

    /**
     * server to client
     */
    exports.SET_COLOR = {
        type: "SET_COLOR",
        data: {
            game_id: null,
            player_id: null,
            color: null
        }
    }

    /**
     * server to client
     */
    exports.SET_MRX = {
        type: "SET_MRX",
        data: {
            player_id: null
        }
    }
})(typeof exports === "undefined" ? (this.LobbyMessages = {}) : exports);
//if exports is undefined, we are on the client; else the server