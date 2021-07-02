(function(exports) {

    /**
     * client to server: connect and join game
     * @typedef {Object} CONNECTED
     * 
     */
    exports.CONNECTED = {
        type: "CONNECTED",
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

    exports.SETMRX = {
        type: "SETMRX",
        data: {
            token: null,
            mr_x: null
        }
    }

})(typeof exports === "undefined" ? (this.Messages = {}) : exports);
//if exports is undefined, we are on the client; else the server