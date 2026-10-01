// Friday, January 15, 2027, 5:01 PM Eastern (EST, UTC-5)
const TARGET = new Date("2027-01-15T17:01:00-05:00").getTime();

const $ = (id) => document.getElementById(id);
const pad = (n) => String(n).padStart(2, "0");

// --- Background photos -------------------------------------------------------
// photos.json is generated at deploy time from the private photos repo.

const loaded = [];   // URLs that have finished downloading
let queue = [];      // shuffled play order; refilled when empty
let current = null;

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function nextPhoto() {
  if (loaded.length === 0) return;
  if (queue.length === 0) {
    queue = shuffle(loaded.slice());
    // avoid showing the same photo twice in a row across reshuffles
    if (queue.length > 1 && queue[queue.length - 1] === current) queue.unshift(queue.pop());
  }
  current = queue.pop();
  $("bg").style.backgroundImage = `url("${current}")`;
}

fetch("photos.json")
  .then((r) => (r.ok ? r.json() : []))
  .then((files) => {
    shuffle(files).forEach((f) => {
      const url = `photos/${f}`;
      const img = new Image();
      img.onload = () => {
        loaded.push(url);
        if (!current) nextPhoto();
      };
      img.src = url;
    });
  })
  .catch(() => {});

// --- Countdown ---------------------------------------------------------------

let finished = false;

function tick() {
  const diff = TARGET - Date.now();

  if (diff <= 0) {
    if (!finished) {
      finished = true;
      $("countdown").hidden = true;
      $("done").hidden = false;
      $("bg").style.display = "none";
      $("shade").style.display = "none";
    }
    return;
  }

  const s = Math.floor(diff / 1000);
  $("days").textContent = Math.floor(s / 86400);
  $("hours").textContent = pad(Math.floor((s % 86400) / 3600));
  $("minutes").textContent = pad(Math.floor((s % 3600) / 60));
  $("seconds").textContent = pad(s % 60);

  nextPhoto();
}

tick();
// align ticks to the wall-clock second so the seconds digit and photo change together
setTimeout(() => {
  tick();
  setInterval(tick, 1000);
}, 1000 - (Date.now() % 1000));
