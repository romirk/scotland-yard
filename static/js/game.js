/**
 * Front end logic for Scotland Yard.
 *
 * @author Romir Kulshrestha <r.kulshrestha@student.tudelft.nl>
 * @author Bhavee Sarna
 * @version 0.1.1a
 */

import Logger from "./logger.js";
import Renderer from "./renderer.js";

/** @typedef { import('./constants').Player } Player */
/** @typedef { import('./constants').Wallet } Wallet */

const logger = new Logger(document.getElementById("log"));
const renderer = new Renderer(document.getElementById("canvas"), logger);

/**
 * Front-end client for Scotland Yard.
 */
class ScotlandYardGameClient {
  /** @readonly */
  static VERSION = "0.1.1a";

  #socket;

  #game_id;
  #player_id;
  #player_name;
  #player_color;
  #location;
  /** @type {Wallet} */
  #wallet;

  #game_info = {};

  /** @type {Object.<string, Player>} */
  #players = {};

  /** @type {number[][][]} */
  #map_data;
  /** @type {number[][]} */
  #coordinates;

  /** @type {string[]} */
  #move_order = [];
  #turn = 0;
  #cycle = 0;
  #state = "IDLE";

  /**
   *
   * @param {WebSocket} socket
   * @param {Player} player_info
   */
  constructor(socket, player_info) {
    this.#socket = socket;
    this.#game_id = player_info.game_id;
    this.#player_id = player_info.player_id;
    this.#player_name = player_info.name;
    this.#player_color = player_info.color;
    this.#location = player_info.location;
    this.#wallet = player_info.wallet;

    this.#configure_ws();
    this.#get_map_data();

    logger.clear();
    logger.log(`Scotland Yard v${ScotlandYardGameClient.VERSION}`, "info");
    logger.log(`Connected to game ${this.#game_id}`);
    logger.log_html(
      `<br>You are <span class=turn>${
        this.str
      }</span> connected as <span class=turn>${this.#player_id}<span>`
    );
    logger.log(`Type HELP for more options.`, "warn");
  }

  get state() {
    return this.#state;
  }

  get turn() {
    return this.#turn;
  }

  get cycle() {
    return this.#cycle;
  }

  get name() {
    return this.#player_name;
  }

  get color() {
    return this.#player_color;
  }

  get location() {
    return this.#location;
  }

  get game_id() {
    return this.#game_id;
  }

  get player_id() {
    return this.#player_id;
  }

  get str() {
    return `${this.#player_name} (${this.#player_color}) @ ${this.#location}`;
  }

  get map_data() {
    return this.#map_data;
  }

  get coordinates() {
    return this.#coordinates;
  }

  /**
   * Asynchronously retrieve map data from server.
   */
  #get_map_data() {
    $.getJSON("/map", (data) => {
      this.#map_data = data.map_data;
      this.#coordinates = data.coordinates;
      logger.log(`Map data loaded.`, "debug");
      this.render();
    });
  }

  /**
   * Configure WebSocket functions.
   */
  #configure_ws() {
    this.#socket.onclose = function (event) {
      logger.log("Connection closed", "error");
      window.location.assign("/");
    };

    this.#socket.onmessage = (e) => this.#game_ws_handler(e);

    this.#socket.onopen = (e) => {
      console.log("Socket opened");
      this.#send("GET_PLAYER_INFO");
      this.#send("GET_PLAYER_INFO ALL");
    };
  }

  /**
   * Send a message to the server over WebSocket.
   * @param {string} msg message
   */
  #send(msg) {
    logger.log(msg, "debug");
    this.#socket.send(msg);
  }

  // #advance_turn() {
  //   this.#turn_count++;
  // }

  /**
   * Handle incoming messages from the server.
   * @param {MessageEvent} event
   */
  #game_ws_handler(event) {
    const msg = event.data;
    const tokens = msg.split(" ");
    const command = tokens[0];

    logger.log(msg, "debug");

    switch (command) {
      case "PLAYER_MOVED":
        let T = msg.split(" ");
        let id = T[1];
        let cycle = T[2];
        //TODO: record ticket log
        let player_location = T[4];

        // this.#advance_turn();
        if (this.cycle !== cycle) {
          logger.log(`Cycle mismatch: ${this.cycle} | ${cycle}`, "error");
        }

        if (player_location !== undefined && player_location !== "") {
          this.#players[id].location = player_location;
        }

        if (this.#player_color === "X") this.#send("GET_PLAYER_INFO");
        this.render();
        break;

      case "GAME_INFO":
        let game_info = JSON.parse(msg.split("GAME_INFO ")[1]);
        this.#game_info = game_info;
        this.#move_order = game_info.move_order;
        break;

      case "PLAYER_INFO":
        let player_info = JSON.parse(msg.split("PLAYER_INFO ")[1]);
        console.log(player_info);
        for (const player_id in player_info) {
          this.#players[player_id] = player_info[player_id];

          if (
            player_id === this.#player_id &&
            player_info[player_id].location === undefined
          ) {
            this.#players[player_id].location = this.#location;
          }
        }

        this.render();
        break;

      case "GAME_STARTING":
        this.#send("GET_GAME_INFO");
        this.#send("GET_PLAYER_INFO ALL");
        this.render();
        break;

      case "DENIED":
        logger.log(`${msg}`, "error");
        break;

      case "ERROR":
        logger.log(msg.split("ERROR - ")[1], "error");
        break;
      default:
        break;
    }
  }

  /**
   * Request a move from the server.
   * @param {string} ticket_type ticket type
   * @param {number} target_location destination
   * @returns {void}
   */
  move(ticket_type, target_location) {
    if (this.#state !== "PLAYING") {
      return;
    }

    if (this.#wallet[ticket_type] === 0) {
      logger.log(`You don't have any ${ticket_type} tickets!`, "warn");
      return;
    }

    if (this.#location === target_location) {
      logger.log(`You're already at ${target_location}!`, "warn");
      return;
    }

    if (this.#move_order[this.turn] !== this.#player_id) {
      logger.log(
        `It's not your turn! It's ${this.#move_order[this.turn]}'s turn.`,
        "warn"
      );
      return;
    }

    this.#send(`MOVE ${ticket_type} ${target_location}`);
  }

  /**
   * Parse console input.
   * @param {string} msg input
   * @returns {void}
   */
  parse(msg) {
    msg = msg.trim().toLowerCase();
    let tokens = msg.split(" ");
    switch (tokens[0]) {
      case "render":
        this.render();
        return;
      case "clear":
        logger.clear();
        return;
      case "debug":
        if (tokens.length < 2) return;
        switch (tokens[1]) {
          case "on":
            logger.debug = true;
            break;

          case "off":
            logger.debug = false;
            break;
          default:
            break;
        }
        logger.log(`Debug mode is ${logger.debug ? "on" : "off"}`);
        return;

      default:
        break;
    }

    logger.log(msg, "info");
    this.#send(msg);
  }

  /**
   * Render UI.
   */
  render() {
    renderer.render(this.#map_data, this.#coordinates, this.#players);
  }
}

$(document).ready(() => {
  $.getJSON("/info", (data) => {
    const player_info = data;
    window.GAME_ID = player_info.game_id;
    const ws_url = `${location.protocol === "https:" ? "wss" : "ws"}://${
      window.location.host
    }/ws/game/${player_info.game_id}/${player_info.player_id}`;
    player_info.state = "new";
    const socket = new WebSocket(ws_url);
    console.log(ws_url, player_info);

    const game = new ScotlandYardGameClient(socket, player_info);

    const commandbox = document.getElementById("ws-command");
    window.addEventListener("keyup", (event) => {
      if (event.key === "Enter") {
        game.parse(commandbox.innerText);
        commandbox.innerText = "";
        commandbox.focus();
      }
    });
    commandbox.focus(); //autofocus on commandbox
  });
});

export default ScotlandYardGameClient;
