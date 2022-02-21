import { TRANSIT_COLORS } from "./constants.js";

class Renderer {
  #canvas;
  #ctx;
  #width;
  #height;
  #margin = 50;

  #limits = {};

  #logger;

  line_width = 3;
  stroke_color = "#00F";

  constructor(canvas, logger) {
    this.#canvas = canvas;
    this.#ctx = this.#canvas.getContext("2d");
    this.#width = canvas.clientWidth;
    this.#height = canvas.clientHeight;
    this.#ctx.imageSmoothingEnabled = false;
    this.#logger = logger;
  }

  #compute_limits(coordinates) {
    this.#width = this.#canvas.clientWidth;
    this.#height = this.#canvas.clientHeight;
    this.#canvas.width = this.#width;
    this.#canvas.height = this.#height;

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

  #compute_scaling() {
    return {
      x: (0.85 * this.#width) / (this.#limits.max_x - this.#limits.min_x),
      y: (0.85 * this.#height) / (this.#limits.max_y - this.#limits.min_y),
    };
  }

  #transform_origin(x, y) {
    const scaling = this.#compute_scaling();
    return {
      x: (x - this.#limits.min_x) * scaling.x + 50,
      y: (y - this.#limits.min_y) * scaling.y + 50,
    };
  }

  render(map_data, coordinates, players) {
    this.#ctx.resetTransform();
    this.#compute_limits(coordinates);
    const scaling = this.#compute_scaling();
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
    // this.#ctx.scale(scaling.x / 10, scaling.y / 10);
    this.#ctx.beginPath();
    this.#ctx.arc(0, 0, this.line_width * 1.5, 0, 2 * Math.PI);
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.fillStyle = "#00f";
    this.#ctx.fill();
  }

  draw_transit(p1, p2, scaling, transit_type) {
    let offset = [0, 0];

    if (transit_type !== 0) {
      let slope = (p2[1] - p1[1]) / (p2[0] - p1[0]);
      if (Math.abs(slope) > 1) {
        offset = [0, 1.5 * this.line_width * (transit_type == 1 ? 1 : -1)];
      } else {
        offset = [this.line_width * 1.5 * (transit_type == 1 ? 1 : -1), 0];
      }
    }

    p1 = [p1[0] * scaling.x + offset[0], p1[1] * scaling.y + offset[1]];
    p2 = [p2[0] * scaling.x + offset[0], p2[1] * scaling.y + offset[1]];

    let scale = 1;
    let mid;
    if (Math.abs(p1[0] - p2[0]) < Math.abs(p1[1] - p2[1])) {
      if (p2[1] < p1[1]) scale = -1;
      mid = [p2[0], scale * Math.abs(p1[0] - p2[0]) + p1[1]];
    } else {
      if (p2[0] < p1[0]) scale = -1;
      mid = [scale * Math.abs(p2[1] - p1[1]) + p1[0], p2[1]];
    }

    this.#ctx.beginPath();
    this.#ctx.moveTo(p1[0], p1[1]);
    this.#ctx.lineTo(mid[0], mid[1]);
    this.#ctx.lineTo(p2[0], p2[1]);
    this.#ctx.strokeStyle = TRANSIT_COLORS[transit_type];
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.stroke();
  }

  draw_line(p1, p2, color) {
    this.#ctx.beginPath();
    this.#ctx.moveTo(p1[0], p1[1]);
    this.#ctx.lineTo(p2[0], p2[1]);
    this.#ctx.strokeStyle = color;
    this.#ctx.lineWidth = this.line_width;
    this.#ctx.stroke();
  }

  draw_players(players, coordinates, scaling) {
    for (const player_id in players) {
      const player = players[player_id];

      if (player.location === undefined) {
        continue;
      }

      let player_loc = player.location;

      let coords = coordinates[player_loc];
      console.log(player_id, players, coords);
      this.#ctx.beginPath();
      this.#ctx.arc(
        coords[0] * scaling.x,
        coords[1] * scaling.y,
        this.line_width * 1.5,
        0,
        2 * Math.PI
      );
      this.#ctx.lineWidth = this.line_width;
      this.#ctx.fillStyle = player.color === "X" ? "#222" : player.color;
      this.#ctx.fill();
    }
  }

  draw_board(map_data, coordinates, scaling) {
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
