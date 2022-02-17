import anime from "./anime.es.js";

function copyToClipboard(elem) {
  // create hidden text element, if it doesn't already exist
  var targetId = "_hiddenCopyText_";
  var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
  var origSelectionStart, origSelectionEnd;
  var temp = false;
  if (isInput) {
    // can just use the original source element for the selection and copy
    target = elem;
    origSelectionStart = elem.selectionStart;
    origSelectionEnd = elem.selectionEnd;
  } else {
    // must use a temporary form element for the selection and copy
    temp = true;
    target = document.getElementById(targetId);
    if (!target) {
      var target = document.createElement("textarea");
      target.style.position = "absolute";
      target.style.left = "-9999px";
      target.style.top = "0";
      target.id = targetId;
      document.body.appendChild(target);
    }
    target.textContent = elem.textContent;
  }
  // select the content
  var currentFocus = document.activeElement;
  target.focus();
  target.setSelectionRange(0, target.value.length);

  // copy the selection
  var succeed;
  try {
    succeed = document.execCommand("copy");
  } catch (e) {
    succeed = false;
  }
  // restore original focus
  if (currentFocus && typeof currentFocus.focus === "function") {
    currentFocus.focus();
  }

  if (isInput) {
    // restore prior selection
    elem.setSelectionRange(origSelectionStart, origSelectionEnd);
  } else {
    // clear temporary content
    target.textContent = "";
  }
  if (temp) target.remove();
  return succeed;
}

const overlay = {
  on: () => (document.getElementById("start-overlay").style.display = "block"),
  off: () => (document.getElementById("start-overlay").style.display = "none"),
};

function circlePath(cx, cy, r) {
  return (
    "M " +
    cx +
    " " +
    cy +
    " m -" +
    r +
    ", 0 a " +
    r +
    "," +
    r +
    " 0 1,0 " +
    r * 2 +
    ",0 a " +
    r +
    "," +
    r +
    " 0 1,0 -" +
    r * 2 +
    ",0"
  );
}

function linear_gradient(
  target,
  to,
  duration = 1000,
  elem = document.getElementById("layout"),
  callback = () => {}
) {
  console.log(target, to);
  let a = anime({
    targets: target,
    start: to.start,
    end: to.end,
    deg: to.deg,
    loop: false,
    duration: duration,
    direction: "normal",
    easing: "easeInOutSine",
    update: (anim) => {
      elem.style.background = `linear-gradient(${target.deg}deg, ${target.start}, ${target.mid}, ${target.end}) center / cover`;
      console.log(Math.round(anim.progress) + "%");
    },
    complete: callback,
  });
  a.play();
  setTimeout(callback, duration);
  console.log(a);
}

function cancelAnimation(animation) {
  console.log(anime.running);
  let activeInstances = anime.running;
  let index = activeInstances.indexOf(animation);
  activeInstances.splice(index, 1);
  animation.pause();
}

function cancelAllAnimations() {
  anime.running.forEach(cancelAnimation);
}

export {
  copyToClipboard,
  overlay,
  circlePath,
  linear_gradient,
  cancelAnimation,
  cancelAllAnimations,
};
