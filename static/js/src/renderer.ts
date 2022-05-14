import Logger from "./logger";

const TRANSIT_COLORS = ["#f7a73e", "green", "red", "black"];

class Renderer {
    #canvas: HTMLCanvasElement;
    #ctx: CanvasRenderingContext2D;
    #width: number;
    #height: number;
    #margin = 50;

    line_width = 3;
    stroke_color = "#000";


    #scaling = (x: number, y: number) => {
        return {
            x: x * this.#width / (this.#width + this.#margin * 2),
            y: y * this.#height / (this.#height + this.#margin * 2)
        };
    };

    constructor(canvas: HTMLCanvasElement, logger: Logger) {
        this.#canvas = canvas;
        this.#ctx = this.#canvas.getContext('2d');
        this.#width = canvas.width;
        this.#height = canvas.height;
        this.#ctx.imageSmoothingEnabled = false;
    }

    draw_transit(p1, p2, color) {
        console.log(p1, p2);
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
        this.#ctx.strokeStyle = color;
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

    draw_board(map_data, coordinates) {
        this.#ctx.clearRect(-1000, -1000, 2000, 2000); //TODO: Fix this hack
        let c = 0;
        let data = map_data;
        data.forEach((station) => {
            let t = 0;
            station.forEach((neighbour_set) => {
                neighbour_set.forEach((neighbour) => {
                    if (neighbour < coordinates.length)
                        this.draw_line(coordinates[c], coordinates[neighbour - 1], TRANSIT_COLORS[t]);
                });
                t++;
            });

            c++;
        });
        for (let i = 0; i < coordinates.length; i++) {
            this.#ctx.beginPath();
            this.#ctx.arc(coordinates[i][0], coordinates[i][1], this.line_width * 1.5, 0, 2 * Math.PI);
            this.#ctx.lineWidth = this.line_width;
            this.#ctx.fillStyle = "#fff";
            this.#ctx.fill();
            this.#ctx.arc(coordinates[i][0], coordinates[i][1], this.line_width * 1.5, 0, 2 * Math.PI);
            this.#ctx.strokeStyle = this.stroke_color;
            this.#ctx.stroke();
            this.#ctx.lineWidth = 1;
            this.#ctx.strokeText(
                String(i + 1),
                coordinates[i][0] - this.line_width,
                coordinates[i][1] - this.line_width * 2
            );
        }
        this.#ctx.beginPath();
        this.#ctx.arc(0, 0, this.line_width * 1.5, 0, 2 * Math.PI);
        this.#ctx.lineWidth = this.line_width;
        this.#ctx.fillStyle = "#00f";
        this.#ctx.fill();
    }

}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function get_scaling(params) {

}

export default Renderer;