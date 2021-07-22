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
const GAME_STATES = { PENDING: 1, RUNNING: 2, STOPPED: 3 }
const ticket_indices = { 'taxi': 0, 'bus': 1, 'underground': 2, 'special': 3 }; //should this go in mapdata.js and then be required?

const MAP = new Map(mapdata);


/**
 * Scotland Yard Game object
 * @param {string} game_id 
 */
function ScotlandYard(game_id) {

    // private
    const id = game_id;
    let state = GAME_STATES.PENDING;
    /** @type {Player[]} */
    const players = [];
    const available_locations = [34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50];
    const available_colors = ['red', 'blue', 'purple', 'green', 'yellow', 'orange'];
    let moves = 0;
    let turn = 0;
    /** @type {Player} */
    let mrX;

    /**
     * Searches for a player in the list of connected players
     * @param {String} player_id ID of the player to be found
     * @returns {Player} player if found, else undefined
     */
    function getPlayer(player_id) {
        return players.find(player => player.getID() === player_id);
    }

    /**
     * Get player at location.
     * @param {number} location 
     * @returns {Player}
     */
    function getPlayerAt(location) {
        for (const player of players)
            if (player.getLocation() === location)
                return player;
    }

    /**
     *  To check if given player can move from one location to another 
     * @param {String} player_id id of the player
     * @param {number} location 0 indexed targets location 
     * @param {String} ticket type of ticket used to make the move
     * @returns {boolean}
     */
    function isValidMove(player_id, location, ticket) {
        let player = getPlayer(player_id);                                                                  // checks that:
        return player !== undefined                                                                         // player exists
            && ((ticket === "special" && player.isMrX()) || (ticket !== "special"))                         // and is not using a special ticket, unless they are Mr. X
            && player.getTickets(ticket) > 0                                                                // and they have a ticket
            && MAP.getStation(player.getLocation()).getNeighbours(ticket).includes(location)                // and it is possible for the player to move to the target location
            && (!player.isMrX() && getPlayerAt(location) === mrX) || getPlayerAt(location) === undefined;   // and no other detective exists at target
    }

    /**
     * Advance turn.
     */
    function advanceTurn() {
        turn = (turn + 1) % 6;
        if (!turn)
            moves++;
    }

    // getters

    /**
     * Get game id.
     * @returns {string} ID
     */
    this.getID = () => id;

    /**
     * Get connected player IDs
     * @returns {String[]} Player IDs
     */
    this.getPlayerIDs = () => players.map(player => player.getID());

    /**
     * Get connected player names
     * @returns {String[]} Player names
     */
    this.getPlayerNames = () => players.map(player => player.getName());

    /**
     * Get players
     * @returns {object} modified player object
     */
    this.getPlayers = () => players.map(player => { return { name: player.getName(), player_id: player.getID(), color: player.getColor(), isMrX: player.isMrX(), game_id: id } })

    /**
     * Checks if game is active
     * @returns {GameState}
     */
    this.getState = () => state;

    // setters
    this.setColor = (player_id, color) => {
        let player = getPlayer(player_id);
        if(player === undefined) return false;
        if (player.isMrX() && color === 'X') {
            player.setColor('X');
            return true;
        }
        if (!player.isMrX() && available_colors.includes(color)) {
            player.setColor(color);
            return true;
        }
        return false;
    };

    this.setMrX = (player_id) => {
        let player = getPlayer(player_id);
        if (player === undefined)
            throw new Exception("Invalid player ID");
        let index = players.indexOf(player);
        players[0].unsetMrX(player.getColor());
        players.splice(index, 1);
        players.unshift(player);
        player.setMrX();
    };

    // methods

    /**
     * Game start logic
     */
    this.init = () => {
        // precondition checks
        if (players.length !== 6)
            throw new Exception("Invalid number of players.", { "players": players.length });
        if (state !== GAME_STATES.PENDING)
            throw new Exception("Game already initialized");
        
        mrX = players[0];
        moves = 0;
        turn = 0;
        state = GAME_STATES.RUNNING;
    }

    /**
     * Add a player to the game
     * @param {String} id 
     * @param {String} name 
     * @returns {boolean} player was added successfully
     */
    this.addPlayer = (id, name) => {
        console.log("adding " + name);
        if (players.length >= MAX_PLAYERS) throw new Exception("Game is full!");
        if (getPlayer(id) !== undefined) throw new Exception("Player already connected");

        let isMrX = players.length === 0;
        let col;

        if (isMrX) {
            col = 'X';
        } else {
            let col_index = Math.floor(Math.random() * available_colors.length);
            col = available_colors[col_index];

            available_colors.splice(col_index, 1);
        }

        let loc_index = Math.floor(Math.random() * available_locations.length);
        let loc = available_locations[loc_index];

        available_locations.splice(loc_index, 1);

        let newPlayer = new Player(id, name, loc, col, isMrX);

        players.push(newPlayer);
        return { color: col, isMrX: isMrX };
    }

    this.move = (player_id, location, ticket) => {
        let player = getPlayer(player_id);
        if (player === undefined)
            throw new Exception("Invalid player ID");
        if (players[turn] !== player.getID())
            throw new Exception(`Not ${player.getName()}'s turn`);

        if (isValidMove(player_id, location, ticket)) {
            player.discard(ticket);
            player.setLocation(location);
            if (!player.isMrX())
                mrX.gain(ticket);
            advanceTurn();
        }
        else
            throw new Exception("Invalid move");
    }

    this.removePlayer = player_id => {      
        if (state === GAME_STATES.PENDING || state === GAME_STATES.STOPPED) {
            let i = players.map(player => player.getID()).indexOf(player_id);
            console.log(`removing ${player_id} at position ${i}`);
            available_colors.push(players[i].getColor());
            available_locations.push(players[i].getLocation());
            players.splice(i, 1);
            return true;
        }
        this.end();
        return false;
    }

    this.move = (id, location) => {
        // TODO implement move logic
    }

    this.end = () => {
        state = GAME_STATES.STOPPED;
    }
};

module.exports = ScotlandYard;