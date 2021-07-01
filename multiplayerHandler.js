const ScotlandYard = require('./game/scotland_yard');

const games = {};

module.exports.createRoom = (token, name) => {
    let game = new ScotlandYard(token);
    games[token] = game;
    return game.addPlayer({ name: name, id: token });
}

// TODO multiplayer logic