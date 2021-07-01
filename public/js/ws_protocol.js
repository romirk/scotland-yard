(function(exports) {

    /*
     * Server to client: connect and join game
     */
    exports.CONNECTED = {
        type: "CONNECTED",
        data: {
            color: null,
            id: null
        }
    };

})(typeof exports === "undefined" ? (this.Messages = {}) : exports);
//if exports is undefined, we are on the client; else the server