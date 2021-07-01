let Player = require('player');

const SURFACE_MOVE = [3, 8, 13, 18, 24];
const MOVE_LIMIT = 24;

let ScotlandYard = (game_id) => {


    this.game_info = {
        id: game_id,
        number_of_players: 0,
        running: true,
        players: [],
        available_locations: [34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50],
        moves: 0,
        turn: 0
    }

    this.addPlayer = (name, color, isMrX) => {
        let index = Math.floor(Math.random() * this.available_locations.length);
        let loc = this.available_locations[index];
        this.available_locations.splice(index, 1);

        this.game_info.players.forEach(player => {
            if (color == player.color) {
                return false;
            }
            if (isMrX && player.isMrX) {
                return false;
            }
        });

        let newPlayer = new Player(name, color, loc, isMrX);

        if (isMrX)
            this.players.unshift(newPlayer);
        else
            this.players.push(newPlayer);
        return true;
    }
};

module.exports = ScotlandYard;