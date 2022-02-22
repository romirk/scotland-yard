import { TRANSIT_COLORS } from "./constants.js";
import Logger from "./logger.js";

/** @typedef { import('./constants').Player } Player */
/** @typedef { import('./constants').Wallet } Wallet */
/** @typedef { import('./constants').Cartesian } Cartesian */

/**
 * HTML5 Canvas rendering system for Scotland Yard.
 */
class Renderer {
  /**
   * The HTML5 Canvas element.
   */
  #canvas;

  /**
   * The rendering context.
   */
  #ctx;

  /**
   * The canvas width.
   */
  #width;

  /**
   * The canvas height.
   */
  #height;

  /**
   * Screen margins.
   */
  #margin = 50;

  /**
   * Game map data.
   * @type {number[][][]}
   */
  #map_data;
  /**
   * Station coordinate data.
   * @type {number[][]}
   */
  #coordinates;

  #limits = {};

  /** @type {Cartesian} */
  #scale = { x: 1, y: 1 };

  #logger;

  line_width = 3;
  stroke_color = "#00F";

  /**
   * Creates an instance of {@link Renderer}
   * @param {HTMLCanvasElement} canvas      HTML5 Canvas element to render the game on.
   * @param {number[][][]}      map_data    game map data.
   * @param {number[][]}        coordinates coordinate data for all stations.
   * @param {Logger}            logger      logging service.
   */
  constructor(canvas, map_data, coordinates, logger = new Logger()) {
    this.#canvas = canvas;
    this.#map_data = map_data;
    this.#coordinates = coordinates;
    this.#ctx = this.#canvas.getContext("2d");
    this.#width = canvas.clientWidth;
    this.#height = canvas.clientHeight;
    this.#ctx.imageSmoothingEnabled = false;
    this.#logger = logger;
  }

  /**
   * Compute bounding box of coordinate data.
   * @returns {void}
   */
  #compute_limits() {
    if (this.#limits.min_x !== undefined) return;

    let min_x = coordinates[0][0];
    let max_x = coordinates[0][0];
    let min_y = coordinates[0][1];
    let max_y = coordinates[0][1];
    for (const coords of coordinates) {
      if (coords[0] < min_x) min_x = coords[0];
      if (coords[0] > max_x) max_x = coords[0];
      if (coords[1] < min_y) min_y = coords[1];
      if (coords[1] > max_y) max_y = coords[1];
    }

    this.#limits = {
      min_x: min_x,
      max_x: max_x,
      min_y: min_y,
      max_y: max_y,
    };
  }

  /**
   * Compute dimensions of canvas element.
   */
  #compute_dimensions() {
    this.#width = this.#canvas.clientWidth;
    this.#height = this.#canvas.clientHeight;
    this.#canvas.width = this.#width;
    this.#canvas.height = this.#height;
  }

  /**
   * Compute scale multipliers for screen dimensions.
   * @returns {Cartesian}
   */
  #compute_scale() {
    this.#scale = {
      x: (0.85 * this.#width) / (this.#limits.max_x - this.#limits.min_x),
      y: (0.85 * this.#height) / (this.#limits.max_y - this.#limits.min_y),
    };
    return this.#scale;
  }

  /**
   * Get transform for plane origin.
   * @param {number} x
   * @param {number} y
   * @returns {Cartesian}
   */
  #transform_origin(x, y) {
    const scaling = this.#compute_scale();
    return {
      x: (x - this.#limits.min_x) * scaling.x + 50,
      y: (y - this.#limits.min_y) * scaling.y + 50,
    };
  }

  /**
   * Render the game UI and board.
   * @param {Object.<string, Player>} players player data
   */
  render(players) {
    this.#ctx.resetTransform();
    this.#compute_limits(coordinates);
    const scaling = this.#compute_scale();
    const origin = this.#transform_origin(0, 0);

    this.#logger.log(`${this.#width}x${this.#height}`, "info");
    this.#logger.log(`${this.#limits.min_x}x${this.#limits.max_x}`, "info");
    this.#logger.log(`${this.#limits.min_y}x${this.#limits.max_y}`, "info");
    this.#logger.log(`${scaling.x}x${scaling.y}`, "info");
    this.#logger.log(`${origin.x}x${origin.y}`, "info");

    this.#ctx.translate(origin.x, origin.y);
    this.#ctx.clearRect(0, 0, this.#width, this.#height);

    this.draw_board(map_data, coordinates, scaling);
    this.draw_players(players, coordinates, scaling);

    this.#ctx.beginPath();
    this.#ctx.arc(0, 0, this.line_width * 1.5, 0, 2 * Math.PI);
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.fillStyle = "#00f";
    this.#ctx.fill();
  }

  /**
   * Draw a subway map-esque transit line between two points.
   * This also offsets transit lines to make sure they don't overlap.
   * @param {number[]} p1 start point
   * @param {number[]} p2 end point
   * @param {number} transit_type Transit type
   */
  draw_transit(p1, p2, transit_type) {
    let offset = [0, 0];

    if (transit_type !== 0) {
      let slope = (p2[1] - p1[1]) / (p2[0] - p1[0]);
      if (Math.abs(slope) > 1) {
        offset = [0, 1.5 * this.line_width * (transit_type == 1 ? 1 : -1)];
      } else {
        offset = [this.line_width * 1.5 * (transit_type == 1 ? 1 : -1), 0];
      }
    }

    p1 = [p1[0] * this.#scale.x + offset[0], p1[1] * this.#scale.y + offset[1]];
    p2 = [p2[0] * this.#scale.x + offset[0], p2[1] * this.#scale.y + offset[1]];

    let direction = 1;
    let mid;
    if (Math.abs(p1[0] - p2[0]) < Math.abs(p1[1] - p2[1])) {
      if (p2[1] < p1[1]) direction = -1;
      mid = [p2[0], direction * Math.abs(p1[0] - p2[0]) + p1[1]];
    } else {
      if (p2[0] < p1[0]) direction = -1;
      mid = [direction * Math.abs(p2[1] - p1[1]) + p1[0], p2[1]];
    }

    this.#ctx.beginPath();
    this.#ctx.moveTo(p1[0], p1[1]);
    this.#ctx.lineTo(mid[0], mid[1]);
    this.#ctx.lineTo(p2[0], p2[1]);
    this.#ctx.strokeStyle = TRANSIT_COLORS[transit_type];
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.stroke();
  }

  /**
   * Draw a colored line.
   * @param {number[]} p1 start point
   * @param {number[]} p2 end point
   * @param {string} color color
   */
  draw_line(p1, p2, color) {
    this.#ctx.beginPath();
    this.#ctx.moveTo(p1[0], p1[1]);
    this.#ctx.lineTo(p2[0], p2[1]);
    this.#ctx.strokeStyle = color;
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.stroke();
  }

  /**
   * Draw players on board.
   * @param {Object.<string, Player>} players player data
   */
  draw_players(players) {
    for (const player_id in players) {
      const player = players[player_id];

      if (player.location === undefined) {
        continue;
      }

      let coords = this.#coordinates[player.location];
      console.log(player_id, players, coords);
      this.#ctx.beginPath();
      this.#ctx.arc(
        coords[0] * this.#scale.x,
        coords[1] * this.#scale.y,
        this.line_width * 1.5,
        0,
        2 * Math.PI
      );
      this.#ctx.lineWidth = this.line_width;
      this.#ctx.fillStyle = player.color === "X" ? "#222" : player.color;
      this.#ctx.fill();
    }
  }

  /**
   * Draw game board.
   */
  draw_board() {
    let c = 0;
    map_data.forEach((station) => {
      let t = 0;
      station.forEach((neighbour_set) => {
        neighbour_set.forEach((neighbour) => {
          if (neighbour < coordinates.length && neighbour > c) {
            this.draw_transit(
              coordinates[c],
              coordinates[neighbour - 1],
              scaling,
              t
            );
          }
        });
        t++;
      });
      c++;
    });
    for (let i = 0; i < coordinates.length; i++) {
      this.#ctx.beginPath();
      this.#ctx.arc(
        coordinates[i][0] * scaling.x,
        coordinates[i][1] * scaling.y,
        this.line_width * 1.5,
        0,
        2 * Math.PI
      );
      this.#ctx.lineWidth = this.line_width;
      this.#ctx.fillStyle = "#fff";
      this.#ctx.fill();
      this.#ctx.arc(
        coordinates[i][0] * scaling.x,
        coordinates[i][1] * scaling.y,
        this.line_width * 1.5,
        0,
        2 * Math.PI
      );
      this.#ctx.strokeStyle = this.stroke_color;
      this.#ctx.stroke();
      this.#ctx.lineWidth = 1;
      this.#ctx.strokeText(
        String(i + 1),
        coordinates[i][0] * scaling.x - this.line_width,
        coordinates[i][1] * scaling.y - this.line_width * 2
      );
    }
  }
}

export default Renderer;
