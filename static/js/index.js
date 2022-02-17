import anime from "./anime.es.js";

function unload() {
  const name = document.getElementById("player_name");
  if (name.value == "" || !name.validity.valid)
    return window.location.replace("/error/invalid%20name");
  setTimeout(() => form.submit(), 1100);
  const grad = {
    c1r: 109,
    c1g: 182,
    c1b: 243,
    c2r: 195,
    c2g: 208,
    c2b: 56,
  };
  const main = document.getElementById("main");
  anime({
    targets: grad,
    c1r: 0,
    c1g: 0,
    c1b: 0,
    c2r: 0,
    c2g: 0,
    c2b: 0,
    duration: 500,
    easing: "easeInQuad",
    update: () =>
      (main.style.background = `linear-gradient(45deg, rgb(${grad.c1r}, ${grad.c1g}, ${grad.c1b}), rgb(${grad.c2r}, ${grad.c2g}, ${grad.c2b})) center / cover`),
  });
  $(".title").fadeOut(500);
  // main.style.animation = "floatout 1s forwards";
}

const form = document.getElementById("start");
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    unload();
  }
});

document.getElementById("start-button").addEventListener("click", (e) => {
  e.preventDefault();
  unload();
});

setTimeout(() => $("#preload").remove(), 1000);
