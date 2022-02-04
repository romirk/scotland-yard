import anime from "./anime.es.js";

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
    c1r: 255,
    c1g: 255,
    c1b: 255,
    c2r: 255,
    c2g: 255,
    c2b: 255,
    duration: 1000,
    easing: "easeInQuad",
    update: () =>
      (main.style.background = `linear-gradient(45deg, rgb(${grad.c1r}, ${grad.c1g}, ${grad.c1b}), rgb(${grad.c2r}, ${grad.c2g}, ${grad.c2b})) center / cover`),
  });
  main.style.animation = "floatout 1s forwards";
}
