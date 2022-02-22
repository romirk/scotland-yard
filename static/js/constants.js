//typedefs
/**
 * @typedef {Object} Cartesian
 * @property {number} x
 * @property {number} y
 */

/**
 * @typedef {Object} Wallet
 * @property {number} taxi
 * @property {number} bus
 * @property {number} underground
 * @property {number=} black
 */

/**
 * @typedef {Object} Player
 * @property {string} player_id
 * @property {string} game_id
 * @property {string} color
 * @property {number} location
 * @property {Wallet} wallet
 * @property {bool} is_host
 */


const gradient = {
  start: "rgba(0, 0, 0, 1)",
  mid: "rgba(0, 0, 0, 0)",
  end: "rgba(0, 0, 0, 1)",
  deg: 45
};

const colorGrads = {
  red: [189, 40, 40],
  purple: [133, 78, 241],
  blue: [30, 73, 169],
  green: [83, 169, 30],
  yellow: [221, 165, 33],
  orange: [207, 106, 19],
  X: [255, 255, 255],
};

const PLAYER_COLORS = ["red", "blue", "purple", "green", "yellow", "orange"];
const TRANSIT_COLORS = ["#f7a73e", "green", "red", "black"];

export { colorGrads, gradient, PLAYER_COLORS, TRANSIT_COLORS };
