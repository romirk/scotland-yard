class Logger {
  static #TYPE_COLORS = {
    error: "red",
    info: "blue",
    debug: "green",
    warn: "orange",
    default: "black",
  };

  #log;
  #log_container;

  constructor(element) {
    this.#log = "";
    this.#log_container = element;
  }

  /**
   * Log to the console on UI
   * @param {String} msg message to be logged
   * @param {String} msg_type message type
   */
  log(msg, msg_type = "default") {
    const span = document.createElement("span");
    span.style.color =
      Logger.#TYPE_COLORS[msg_type] || Logger.#TYPE_COLORS.default;
    span.innerText = msg;
    this.#log_container.appendChild(document.createElement("br"));
    this.#log_container.appendChild(span);
  }

  clear() {
    this.#log = this.#log_container.innerHTML = "";
  }
}

export default Logger;
