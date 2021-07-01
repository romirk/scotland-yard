const Player = require('./player');
const Map = require('./map');
const mapdata = require('./mapdata');

const SURFACE_MOVES = [3, 8, 13, 18, 24];
const MOVE_LIMIT = 24;
const MAX_PLAYERS = 6;

let ScotlandYard = (game_id) => {


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

    this.addPlayer = (con, name, color, isMrX) => {
        if (game_info.number_of_players >= MAX_PLAYERS) return false;

        let index = Math.floor(Math.random() * this.available_locations.length);
        let loc = this.available_locations[index];

        game_info.players.forEach(player => {
            if (color == player.color) {
                return false;
            }
            if (isMrX && player.isMrX) {
                return false;
            }
        });

        this.available_locations.splice(index, 1);

        let newPlayer = new Player(con.id, name, color, loc, isMrX);

        if (isMrX)
            game_info.players.unshift(newPlayer);
        else
            game_info.players.push(newPlayer);
        return true;
    }
};

module.exports = ScotlandYard;