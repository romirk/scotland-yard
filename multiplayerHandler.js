const ScotlandYard = require('./game/scotland_yard');
const Exception = require('./Exceptions');

const games = {};
const players = {};

/**
 * Creates new game.
 * @param {String} token player ID
 * @param {String} name name
 * @returns {boolean} successful
 */
module.exports.createRoom = (token, name) => {
    let game = new ScotlandYard(token);
    games[token] = game;
    players[token] = token;
};

/**
 * Add player to game.
 * @param {String} player_id 
 * @param {String} player_name 
 * @param {String} game_id 
 * @returns {boolean}
 */
module.exports.joinRoom = (player_id, player_name, game_id) => {
    if (players[player_id] !== undefined)
        games[players[player_id]].removePlayer(player_id);

    if (games[game_id] === undefined)
        return false;

    /** @type {boolean} */
    let result = games[game_id].addPlayer(player_id, player_name);
    if (result)
        players[player_id] = game_id;
    return result;
}

module.exports.startGame = game_id => {
    if (games[game_id] === undefined)
        return false;
    try {
        games[game_id].init();
        return true;
    } catch (e) {
        if (e instanceof Exception) {
            console.log("%cERROR: %c" + e.message, "color: red", "color: default");
        } else {
            console.log("Uncaught excpetion in handling multiplayer game start: " + e);
            throw e;
        }
    }
}

module.exports.disconnect = player_id => {
    games[players[player_id]].removePlayer(player_id);
    delete players[player_id];
}

module.exports.gameExists = game_id => games[game_id] !== undefined;
module.exports.getGameWithPlayer = player_id => players[player_id];