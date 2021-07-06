const ScotlandYard = require('./game/scotland_yard');
const Exception = require('./Exceptions');

/** @typedef {string} ID */

/** @type {Object.<ID, ScotlandYard>} */
const games = {};
/** @type {Object.<ID, ID>} */
const players = {};

/**
 * Creates new game.
 * @param {ID} token player ID
 * @returns {Promise} successful, passes newly created game ID
 */
module.exports.createRoom = token => {
    return new Promise((resolve, reject) => {
        let game = new ScotlandYard(token);
        games[token] = game;
        players[token] = token;
        resolve(token);
    });
};

/**
 * Adds a player to a game.
 * @param {ID} player_id 
 * @param {string} player_name 
 * @param {ID} game_id 
 * @returns {Promise}
 */
module.exports.joinRoom = (player_id, player_name, game_id) => {
    return new Promise((resolve, reject) => {
        if (players[player_id] !== undefined)
            games[players[player_id]].removePlayer(player_id);

        if (games[game_id] === undefined) 
            return reject("game does not exist");

        /** @type {boolean} */
        let result = games[game_id].addPlayer(player_id, player_name);
        if (result) {
            players[player_id] = game_id;
            console.log(`${player_name} joined`);
            return resolve();
        } else
            return reject("can't add player to game");
    });
}

/**
 * Starts the game with the given ID
 * @param {ID} game_id 
 */
module.exports.startGame = game_id => {
    if (games[game_id] === undefined)
        return false;
    let game = games[game_id];
    if(game.getState() === 2) {
        // game is running 
        // do nothing
        return;
    }
    else if(game.getState() === 3) {
        // game has ended
        // do nothing, but this is weird so log it
        console.log("tried to start elapsed game: " + game_id);
        return;
    }
    games[game_id].init();
}

/**
 * Disconnects a player from a game.
 * @param {ID} player_id 
 */
module.exports.disconnect = player_id => {
    games[players[player_id]].removePlayer(player_id);
    delete players[player_id];
}

/**
 * Checks if game exists.
 * @param {ID} game_id 
 * @returns {boolean}
 */
module.exports.gameExists = game_id => {
    return games[game_id] !== undefined;
}

/**
 * Gets the game ID a player is associated with.
 * @param {ID} player_id 
 * @returns {ID}
 */
module.exports.getGameWithPlayer = player_id => players[player_id];