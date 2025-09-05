window.onload = function() {
  document.getElementById("streaming").src = "http://192.168.4.1:81/stream";
  initWebSocket();
  initButtons();
  createPlantButtons();
};


var gateway = ws://${window.location.hostname}/ws;
var websocket;
let currentSpeed = 20; // Default speed

function onOpen(event) {
  console.log("WebSocket connection opened");
}

function onClose(event) {
  console.log("WebSocket connection closed");
  setTimeout(initWebSocket, 2000);
}

function initWebSocket() {
  console.log("Trying to open a WebSocket connection...");
  websocket = new WebSocket(gateway);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}

function onMessage(event) {
  console.log(Received: ${event.data});
}

// Initialize Button Events
function initButtons() {
  const buttons = document.querySelectorAll(".button");

  buttons.forEach(button => {
    button.addEventListener("mousedown", () => websocket.send(button.id));
    button.addEventListener("mouseup", () => websocket.send("stop"));
    button.addEventListener("touchstart", () => websocket.send(button.id));
    button.addEventListener("touchend", () => websocket.send("stop"));
  });
}

// Keyboard Control Mapping
const keyActions = {
  w: "forward",
  a: "left",
  s: "backward",
  d: "right"
};

let activeKeys = {};

document.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();
  if (isManualMode && keyActions[key] && !activeKeys[key]) {
    websocket.send(keyActions[key]);
    activeKeys[key] = true;
    console.log(Key Pressed: ${key});
  }
});

document.addEventListener("keyup", (event) => {
  const key = event.key.toLowerCase();
  if (isManualMode && keyActions[key]) {
    websocket.send("stop");
    activeKeys[key] = false;
  }
});

// Mode Toggle
let isManualMode = true;
document.getElementById("modeSwitch").addEventListener("click", function() {
  const modeSwitch = document.getElementById("modeSwitch");
  isManualMode = !isManualMode;

  if (isManualMode) {
    modeSwitch.textContent = "Manual Mode";
    modeSwitch.classList.remove("automated");
    websocket.send("manual");
    toggleManualControls(false);
  } else {
    modeSwitch.textContent = "Automated Mode";
    modeSwitch.classList.add("automated");
    websocket.send("automated");
    toggleManualControls(true);
  }
});

// Enable/Disable Manual Controls
function toggleManualControls(disabled) {
  document.querySelectorAll(".button").forEach(button => {
    button.disabled = disabled;
  });
}

// Speed Control Function
function setSpeed() {
  const speedInput = document.getElementById("speed");
  const speedValue = parseInt(speedInput.value);

  if (isNaN(speedValue) || speedValue < 0 || speedValue > 80) {
    alert("Please enter a valid speed between 0 and 80 RPM.");
    return;
  }

  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(setSpeed:${speedValue});
    currentSpeed = speedValue;
    console.log(Speed set to ${speedValue} RPM);
    alert(Speed set to ${speedValue} RPM);
  } else {
    alert("WebSocket not connected. Try again later.");
  }
}
// Modal Logic
const plantModal = document.getElementById("plantModal");
const openModalBtn = document.getElementById("openModal");
const closeBtn = document.querySelector("#plantModal .close");

openModalBtn.addEventListener("click", () => {
  plantModal.style.display = "block";
});

closeBtn.addEventListener("click", () => {
  plantModal.style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target === plantModal) {
    plantModal.style.display = "none";
  }
});
