const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function draw_transit(p1, p2, color) {
    let scale = 1;
    let mid;
    if(Math.abs(p1[0] - p2[0]) < Math.abs(p1[1] - p2[1])) {
        if(p2[1] < p1[1])
            scale = -1;
        mid = [p2[0], scale * Math.abs(p1[0]-p2[0]) + p1[1]];
    } else {
        if(p2[0] < p1[0])
            scale = -1;
        mid = [scale * Math.abs(p2[1] - p1[1]) + p1[0], p2[1]];
    }
    ctx.moveTo(p1[0], p1[1]);
    ctx.lineTo(mid[0], mid[1]);
    ctx.lineTo(p2[0], p2[1]);
    ctx.strokeStyle = color;
    ctx.strokeWidth = 2;
    ctx.stroke();
}

function draw_board(params) {
    
}