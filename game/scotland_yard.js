const Player = require('./player');
const Map = require('./map');
const mapdata = require('./mapdata');

const SURFACE_MOVES = [3, 8, 13, 18, 24];
const MOVE_LIMIT = 24;
const MAX_PLAYERS = 6;

function ScotlandYard(game_id) {


    const game_info = {
        id: game_id,
        number_of_players: 0,
        running: true,
        players: [],
        available_locations: [34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50],
        moves: 0,
        turn: 0
    }

    const map = new Map(mapdata);

    this.addPlayer = (id, name) => {
        if (game_info.number_of_players >= MAX_PLAYERS) return false;

        let index = Math.floor(Math.random() * game_info.available_locations.length);
        let loc = game_info.available_locations[index];

        game_info.available_locations.splice(index, 1);

        let newPlayer = new Player(id, name, loc);

        game_info.players.push(newPlayer);
        game_info.number_of_players++;
        return true;
    }

    this.removePlayer = id => {
        // TODO remove player logic
        let index = this.getPlayer(id);
        if (index == -1) return false;

        game_info.players.splice(index, 1);
        game_info.number_of_players--;
        if (game_info.number_of_players < 3) this.end();
        return true;
    }

    this.getPlayer = token => {
        return game_info.players.map(player => player.id).findIndex(id => id === token);
    }

    this.setColor = (token, color) => {
        // TODO implement setColor
    };
    this.setMrX = (token) => {
        // TODO implement setMrX
    };

    this.end = () => running = false;

};

module.exports = ScotlandYard;