(function(exports) {

    /**
     * client to server: connect and join game
     * @typedef {Object} CONNECTED
     * 
     */
    exports.CONNECT = {
        type: "CONNECT",
        data: {
            token: null,
            name: null,
            color: null,
            isMrX: false
        }
    };

    exports.ACKNOWLEDGE = {
        type: "ACKNOWLEDGE",
        data: {
            token: null
        }
    }
    
    exports.MOVE_REQUEST = {
        type: "MOVE_REQUEST",
        data: {}
    }

})(typeof exports === "undefined" ? (this.GameMessages = {}) : exports);
//if exports is undefined, we are on the client; else the server