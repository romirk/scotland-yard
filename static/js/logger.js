/**
 * @file Front-end logging.
 */

/**
 * Console-style UI logging system.
 */
class Logger {
  static #TYPE_COLORS = {
    error: "red",
    info: "blue",
    debug: "grey",
    warn: "orange",
    default: "black",
  };

  #log_container;

  /**
   * Sets debug mode.
   * Debug messages are not shown if this is off.
   */
  debug = true;

  /**
   * Creates an instance of a {@link Logger}.
   * @param {HTMLElement} element
   */
  constructor(element = document.getElementById("log")) {
    this.#log_container = element;
  }

  /**
   * Log to the console on UI
   * @param {String} msg message to be logged
   * @param {String} msg_type message type
   */
  log(msg, msg_type = "default") {
    if (!this.debug && msg_type === "debug") return;
    const span = document.createElement("span");
    span.style.color =
      Logger.#TYPE_COLORS[msg_type] || Logger.#TYPE_COLORS.default;
    span.innerText = msg;
    this.#log_container.appendChild(document.createElement("br"));
    this.#log_container.appendChild(span);
  }

  /**
   * Log to the console on UI.
   * @param {String} html html to be logged
   */
  log_html(html) {
    this.#log_container.innerHTML += html;
  }

  /**
   * Clear the log.
   */
  clear() {
    this.#log_container.innerHTML = "";
  }
}

export default Logger;
