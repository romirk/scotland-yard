const Player = require('./player');
const Map = require('./map');
const Exception = require('../Exceptions');
const mapdata = require('./mapdata');

/** @typedef {number} GameState */
/**
 * @typedef GameInfo
 * @type {object}
 * @property {string} id
 * @property {GameState} state
 * @property {Player[]} players
 * @property {number[]} available_locations
 * @property {number} moves
 * @property {numbern} turn
 */

const SURFACE_MOVES = [3, 8, 13, 18, 24];
const MOVE_LIMIT = 24;
const MAX_PLAYERS = 6;
const GAME_STATES = {PENDING: 1, RUNNING: 2, STOPPED: 3}
const ticket_indices = {'taxi': 0, 'bus': 1, 'underground': 2, 'special': 3}; //should this go in mapdata.js and then be required?

const MAP = new Map(mapdata);


/**
 * Scotland Yard Game object
 * @param {string} game_id 
 */
function ScotlandYard(game_id) {
    
    /** @type {GameInfo} */
    const game_info = {
        id: game_id,
        state: GAME_STATES.PENDING,
        players: [],
        available_locations: [34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50],
        available_colors: ['red', 'blue', 'purple', 'green', 'yellow', 'orange'],
        moves: 0,
        turn: 0
    }  

    // private

    /**
     * Searches for a player in the list of connected players
     * @param {String} token ID of the player to be found
     * @returns {number} index of the player in game_info.players if found, else -1
     */
    function getPlayer(token) {
        return game_info.players.findIndex(player => player.id === token);
    }

    /**
     *  To check if given player can move from one location to another 
     * @param {String} token id of the player
     * @param {number} start 0 indexed start location
     * @param {number} end 0 indexed end location 
     * @param {String} ticket type of ticket used to make the move
     * @returns {boolean}
     */
    function validMove(token, start, end, ticket){
        let index = getPlayer(token);
        return index !== -1 
            && game_info.players[index].getTickets(ticket) > 0 
            && MAP.getStation(start).getNeighbours(ticket).includes(end);
        //player exists, player has the required ticket, there exists a path from start to end that requires this ticket
    }

    // getters

    /**
     * Get connected players
     * @returns {String[]} Player IDs
     */
    this.getPlayers = () => game_info.players.map(player => player.id);

    /**
     * Checks if game is active
     * @returns {GameState}
     */
    this.getState = () => game_info.state;

    // setters
    this.setColor = (token, color) => {
        // TODO delegate setColor to Player
    };

    this.setMrX = (token) => {
        // TODO delegate setMrX to Player
        let index = getPlayer(token);
        if(index === -1) return false;
        if(index !== 0){
            let newX = game_info.players[index];
            game_info.players[0].unsetMrX(newX.getColor());            
            newX.setMrX();
            game_info.players.splice(index, 1);
            game_info.players.unshift(newX);
            return true;
        }        
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
        console.log("adding " + name);
        if (game_info.players.length >= MAX_PLAYERS) throw new Exception("Game is full!");
        if (getPlayer(id) !== -1) throw new Exception("Player already connected");

        let isMrX = game_info.players.length === 0;
        let color = isMrX ? 'X' : game_info.available_colors[Math.floor(Math.random() * game_info.available_colors.length)];

        let loc_index = Math.floor(Math.random() * game_info.available_locations.length);
        let loc = game_info.available_locations[loc_index];

        game_info.available_locations.splice(loc_index, 1);

        let newPlayer = new Player(id, name, loc, color, isMrX);

        game_info.players.push(newPlayer);
        return {color: color, isMrX: isMrX};
    }

    this.removePlayer = token => {
        //TODO remove player logic

    }

    this.move = (id, location) => {
        // TODO implement move logic
    }
};

module.exports = ScotlandYard;