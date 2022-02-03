const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
ctx.canvas.height = window.innerHeight * 0.9;
ctx.canvas.width = window.innerWidth * 0.6;
const MARGIN = 50;
const SPACING = 50;

const SCALING =
  Math.min(
    ctx.canvas.width / (LIMITS.max[0] - LIMITS.min[0]),
    ctx.canvas.height / (LIMITS.max[1] - LIMITS.min[1])
  ) * 0.9;

for (let i = 0; i < STATIONS.length; i++) {
  STATIONS[i][0] *= SCALING;
  STATIONS[i][1] *= SCALING;
}
ctx.translate(
  MARGIN - LIMITS.min[0] * SCALING + MARGIN,
  MARGIN - LIMITS.min[1] * SCALING
);

const LINE_WIDTH = 3;
const STROKE_COLOR = "blue";
const TRANSIT_COLORS = ["#f7a73e", "green", "red", "black"];
let draw_until = STATIONS.length;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function draw_transit(p1, p2, color) {
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

  ctx.beginPath();
  ctx.moveTo(p1[0], p1[1]);
  ctx.lineTo(mid[0], mid[1]);
  ctx.lineTo(p2[0], p2[1]);
  ctx.strokeStyle = color;
  ctx.lineWidth = LINE_WIDTH;
  ctx.stroke();
}

function draw_line(p1, p2, color) {
  ctx.beginPath();
  ctx.moveTo(p1[0], p1[1]);
  ctx.lineTo(p2[0], p2[1]);
  ctx.strokeStyle = color;
  ctx.lineWidth = LINE_WIDTH;
  ctx.stroke();
}

function draw_board() {
  let c = 0;
  let data = MAP_DATA;
  data.forEach((station) => {
    if (c < draw_until) {
      let t = 0;
      station.forEach((neighbour_set) => {
        neighbour_set.forEach((neighbour) => {
          if (neighbour < STATIONS.length)
            draw_transit(
              STATIONS[c],
              STATIONS[neighbour - 1],
              TRANSIT_COLORS[t]
            );
        });
        t++;
      });
    }
    c++;
  });
  for (let i = 0; i < STATIONS.length; i++) {
    ctx.beginPath();
    ctx.arc(STATIONS[i][0], STATIONS[i][1], LINE_WIDTH * 1.5, 0, 2 * Math.PI);
    ctx.lineWidth = LINE_WIDTH;
    ctx.fillStyle = "#fff";
    ctx.fill();
    ctx.arc(STATIONS[i][0], STATIONS[i][1], LINE_WIDTH * 1.5, 0, 2 * Math.PI);
    ctx.strokeStyle = STROKE_COLOR;
    ctx.stroke();
    ctx.lineWidth = 1;
    ctx.strokeText(
      i + 1,
      STATIONS[i][0] - LINE_WIDTH,
      STATIONS[i][1] - LINE_WIDTH * 2
    );
  }
  ctx.beginPath();
  ctx.arc(0, 0, LINE_WIDTH * 1.5, 0, 2 * Math.PI);
  ctx.lineWidth = LINE_WIDTH;
  ctx.fillStyle = "#00f";
  ctx.fill();
}

function draw_ui() {
  ctx.clearRect(-1000, -1000, 2000, 2000);
  draw_board();
}


canvas.addEventListener("onmouseup", e => console.log(e.clientX, e.clientY));


draw_ui();
