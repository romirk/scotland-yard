const Player = require('./player');
const Map = require('./map');
const Exception = require('../Exceptions');
const mapdata = require('./mapdata');

const SURFACE_MOVES = [3, 8, 13, 18, 24];
const MOVE_LIMIT = 24;
const MAX_PLAYERS = 6;

function ScotlandYard(game_id) {


    const game_info = {
        id: game_id,
        running: true,
        players: [],
        available_locations: [34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50],
        moves: 0,
        turn: 0
    }

    const map = new Map(mapdata);


    // private

    /**
     * Searches for a player in the list of connected players
     * @param {String} token ID of the player to be found
     * @returns {number} index of the player in game_info.players if found, else -1
     */
    function getPlayer(token) {
        return game_info.players.findIndex(player => player.id === token);
    }

    // getters

    /**
     * Get connected players
     * @returns {String[]} Player IDs
     */
    this.getPlayers = () => game_info.players.map(player => player.id);

    /**
     * Checks if game is active
     * @returns {boolean}
     */
    this.isRunning = () => game_info.running;

    // setters
    this.setColor = (token, color) => {
        // TODO delegate setColor to Player
    };
    this.setMrX = (token) => {
        // TODO delegate setMrX to Player
    };

    // methods

    /**
     * Game start logic
     */
    this.init = () => {
        // precondition checks
        if (game_info.players.length !== 6)
            throw new Exception("Invalid number of players.", { "players": game_info.players.length });
        // TODO init logic
    }

    /**
     * Add a player to the game
     * @param {String} id 
     * @param {String} name 
     * @returns {boolean} player was added successfully
     */
    this.addPlayer = (id, name) => {
        if (game_info.players.length >= MAX_PLAYERS) return false;
        if (getPlayer(id) !== -1) return false;

        let index = Math.floor(Math.random() * game_info.available_locations.length);
        let loc = game_info.available_locations[index];

        game_info.available_locations.splice(index, 1);

        let newPlayer = new Player(id, name, loc);

        game_info.players.push(newPlayer);
        return true;
    }

    this.removePlayer = token => {
        //TODO remove player logic

    }

    this.move = (id, location) => {
        // TODO implement move logic
    }
};

module.exports = ScotlandYard;