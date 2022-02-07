const game = {
  canvas: document.createElement("canvas"),
  init: function () {
    this.context = this.canvas.getContext("2d");
    this.canvas.classList.add("board");
    document
      .getElementById("board-wrap")
      .insertBefore(
        this.canvas,
        document.getElementById("board-wrap").childNodes[0]
      );
  },
};

game.init();
