const ScotlandYard = require('./game/scotland_yard');

const games = {};
const players = {};

module.exports.createRoom = (token, name) => {
    let game = new ScotlandYard(token);
    games[token] = game;
    players[token] = token;
    return game.addPlayer(token, name);
};

module.exports.joinRoom = (player_id, player_name, game_id) => {
    if (players[player_id] !== undefined)
        games[players[player_id]].removePlayer(player_id);

    if (games[game_id] === undefined)
        return false;

    let result = games[game_id].addPlayer(player_id, player_name);
    if (result)
        players[player_id] = game_id;
    return result;
}

module.exports.disconnect = player_id => {
    games[players[player_id]].removePlayer(player_id);
    delete players[player_id];
}

module.exports.getGameWithPlayer = player_id => players[player_id];