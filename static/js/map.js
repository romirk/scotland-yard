const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
ctx.canvas.height = window.innerHeight - 30;
ctx.canvas.width = window.innerWidth - 30;
ctx.translate(700, 300);
const MARGIN = 100;
const SPACING = 50;
const SCALING = 50;
// const STATIONS = [];
const LINE_WIDTH = 3;
const STROKE_COLOR = "purple";

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

function draw_board() {
  for (let i = 0; i < STATIONS.length; i++) {
    STATIONS[i][0] *= SCALING;
    STATIONS[i][1] *= SCALING;
  }
  let c = 0;
  let data = MAP_DATA;
  data.forEach((station) => {
    neighbours = new Set();
    station.forEach((neighbour_set) => {
      neighbour_set.forEach((neighbour) => neighbours.add(neighbour));
    });
    console.log(neighbours);
    neighbours.forEach((neighbour) => {
      console.log(neighbour);
      if (neighbour < STATIONS.length)
        draw_transit(STATIONS[c], STATIONS[neighbour - 1], STROKE_COLOR);
    });
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
  draw_board();
}

draw_ui();
