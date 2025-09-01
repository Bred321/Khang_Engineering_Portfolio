window.onload = document.getElementById("streaming").src ="http://192.168.4.1:81/stream";

var button = document.querySelector(".button");
const buttons = document.querySelectorAll('.button');
var gateway = `ws://${window.location.hostname}/ws`;
var websocket;

window.addEventListener('load', onLoad);
// init WebSocket
function onOpen(event) {
  console.log('Connection opened');
}
function onClose(event) {
  console.log('Connection closed');
  setTimeout(initWebSocket, 2000);
}
function initWebSocket() {
    console.log('Trying to open a WebSocket connection...');
    websocket = new WebSocket(gateway);
    websocket.onopen    = onOpen;
    websocket.onclose   = onClose;
    websocket.onmessage = onMessage;
}

function onMessage(event) {
  console.log(`Received a notification from ${event.origin}`);
  console.log(event);
}

function initButtons() {
  var buttons = document.querySelectorAll(".button");
  buttons.forEach(button => {
    button.addEventListener('mousedown', function(event) {
      websocket.send(event.target.id);
    });
    button.addEventListener('mouseup', function(event) {
      websocket.send('stop');
    });
    button.addEventListener('touchstart', function(event) {
      websocket.send(event.target.id);
    });
    button.addEventListener('touchend', function(event) {
      websocket.send('stop');
    });
  });
}

function onLoad(event) {
  initWebSocket();
  initButtons();
}
function buttonpressed (x) {
  websocket.send (x);
}
var keyActions = {
  w: function () {
    buttonpressed('forward');
  },
  a: function () {
    buttonpressed('left');
  },
  s: function () {
    buttonpressed('backward');
  },
  d: function () {
    buttonpressed('right');
  },
};

var keys = {};

document.addEventListener("keydown", function(event) {
  var key = event.key.toLowerCase();
  if (isManualMode) {
    if (keyActions[key] && !keys[key]) { // Check if key is not already pressed
      keyActions[key]();
      keys[key] = true; // Mark key as pressed
      console.log("Key pressed:", key);
    }
  }
});

document.addEventListener("keyup", function(event) {
  var key = event.key.toLowerCase();
  if (isManualMode) {
    if (keys[key]) {
      keys[key] = false; // Mark key as released
      websocket.send("stop");
    }
  }
});
// Track the current mode
let isManualMode = true;

// Handle toggle button click
document.getElementById('modeSwitch').addEventListener('click', function () {
  const modeSwitch = document.getElementById('modeSwitch');
  isManualMode = !isManualMode; // Toggle the mode

  if (isManualMode) {
    modeSwitch.textContent = 'Manual Mode';
    modeSwitch.classList.remove('automated');
    websocket.send('manual'); // Notify the ESP32-CAM
    disableManualControls(false); // Enable manual controls
  } else {
    modeSwitch.textContent = 'Automated Mode';
    modeSwitch.classList.add('automated');
    websocket.send('automated'); // Notify the ESP32-CAM
    disableManualControls(true); // Disable manual controls
  }
});

// Function to enable/disable manual controls
function disableManualControls(disable) {
  buttons.forEach(button => {
    button.disabled = disable; // Disable or enable buttons
  });
  
}