class Logger {
    static #TYPE_COLORS = {
        error: "red",
        info: "blue",
        debug: "green",
        warn: "orange",
        default: "black",
    };

    #log: string;
    #log_element: HTMLElement;

    constructor(element: HTMLElement) {
        this.#log = "";
        this.#log_element = element;
    }

    /**
     * Log to the console on UI
     * @param {String} msg message to be logged
     * @param {String} msg_type message type
     */
    log(msg: string, msg_type: string = "default") {
        this.#log += `<br><span style="color:${Logger.#TYPE_COLORS[msg_type]
            }">${msg}</span>`;
        this.#log_element.innerHTML = this.#log;
    }

    clear() {
        this.#log = this.#log_element.innerHTML = "";
    }
}

export default Logger;