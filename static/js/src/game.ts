import Logger from "./logger";
import Renderer from "./renderer";

const logger = new Logger(document.getElementById("log"));
const renderer = new Renderer(document.getElementById("canvas") as HTMLCanvasElement, logger);


class ScotlandYardGame {
    static VERSION = "0.1 alpha";

    #socket: WebSocket;

    #game_id: string;
    #player_id: string;
    #player_name: string;
    #player_color: string;
    #location: number = -1;

    #game_info: object = {};

    #move_order: string[] = [];
    #turn_count: number = 0;
    #state = "PENDING";

    constructor(socket: WebSocket, game_id: string, player_id: string, player_name: string, player_color: string) {
        this.#socket = socket;
        this.#game_id = game_id;
        this.#player_id = player_id;
        this.#player_name = player_name;
        this.#player_color = player_color;

        this.#configure_ws();

        logger.log(`Scotland Yard v${ScotlandYardGame.VERSION}`, "info");
    }

    #configure_ws() {
        this.#socket.onclose = function (event) {
            logger.log("Connection closed", "error");
            window.location.assign("/");
        };

        this.#socket.onmessage = this.#game_ws_handler;

        this.#socket.onopen = event => {
            console.log("Socket opened");
            this.#send("GET_PLAYER_INFO");
        };

    }

    #send(msg: string) {
        logger.log(msg, "debug");
        this.#socket.send(msg);
    }

    #advance_turn() {
        this.#turn_count++;
    }

    #game_ws_handler(event: MessageEvent) {
        const msg = event.data;
        const tokens = msg.split(" ");
        const command = tokens[0];

        logger.log(msg, "debug");

        switch (command) {
            case "PLAYER_MOVED":
                if (this.#move_order[this.turn] === this.#player_id) {
                    this.#send("GET_PLAYER_INFO");
                }

                this.#advance_turn();

                if (this.#move_order[this.turn] == this.#player_id) {
                    logger.log(`It's your turn!`, "warn");
                }
                break;

            case "GAME_INFO":
                let game_info = JSON.parse(msg.data.split("GAME_INFO ")[1]);
                this.#game_info = game_info;
                this.#move_order = game_info.move_order;
                break;

            case "PLAYER_INFO":
                let player_info = JSON.parse(msg.data.split("PLAYER_INFO ")[1]);
                this.#location = player_info.location;
                break;

            case "GAME_STARTING":
                this.#send("GET_GAME_INFO");
                break;
            default:
                break;
        }
    }




    get state(): string {
        return this.#state;
    }

    get turn(): number {
        return this.#turn_count % 6;
    }

    get cycle(): number {
        return Math.floor(this.#turn_count / 6);
    }

    get name(): string {
        return this.#player_name;
    }

    get color(): string {
        return this.#player_color;
    }

    get location(): number {
        return this.#location;
    }

    get game_id(): string {
        return this.#game_id;
    }

    get player_id(): string {
        return this.#player_id;
    }

}

export default ScotlandYardGame;
