const ScotlandYard = require('./game/scotland_yard');
const Exception = require('./Exceptions');

/** @typedef {string} ID */

/** @type {Object.<ID, ScotlandYard>} */
const games = {};
/** @type {Object.<ID, ID>} */
const players = {};

/**
 * Creates new game.
 * @param {ID} player_id player ID
 * @returns {Promise} successful, passes newly created game ID
 */
module.exports.createRoom = player_id => {
    return new Promise((resolve, reject) => {
        let game = new ScotlandYard(player_id);
        games[player_id] = game;
        players[player_id] = player_id;
        resolve(player_id);
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
        console.log(`joining ${game_id}...`);
        // if (players[player_id] !== undefined) {
        //     try {
        //         games[players[player_id]].removePlayer(player_id);
        //     } catch (error) {
        //         ;
        //     }
        // }
           

        if (games[game_id] === undefined) 
            return reject("game does not exist");

        /** @type {boolean} */
        try {
            let result = games[game_id].addPlayer(player_id, player_name);
            players[player_id] = game_id;
            console.log(`${player_name} joined as ${result.isMrX ? 'Mr. X' : 'a detective'}.`);
            return resolve(result);
        } catch (err) {
            return reject("can't add player to game: " + err.message);
        }
        
            
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

module.exports.move = (game_id, player_id, location, ticket) => {
    // TODO handle multiplayer move
    games[game_id].move(player_id, location, ticket);

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
module.exports.getGameByPlayer = player_id => players[player_id];

module.exports.checkPlayerInGame = (game_id, player_id) => module.exports.getAllPlayerIDsInGame(game_id).includes(player_id);

module.exports.getAllPlayersInGame = game_id => games[game_id].getPlayers();

module.exports.getAllPlayerIDsInGame = game_id => games[game_id].getPlayerIDs();

module.exports.getAllPlayerNamesInGame = game_id => games[game_id].getPlayerNames();

module.exports.setColor = (game_id, player_id, color) => games[game_id].setColor(player_id, color);

module.exports.setMrX = (game_id, player_id) => games[game_id].setMrX(player_id);