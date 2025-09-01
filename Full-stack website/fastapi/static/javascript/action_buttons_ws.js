// JavaScript functionality for AGV Control UI
document.addEventListener("DOMContentLoaded", function () {
    /* Website elements variables */
    const stopButton = document.getElementById("stopBtn");
    const uvOnButton = document.getElementById("setUVOnBtn");
    const uvOffButton = document.getElementById("setUVOffBtn");
    const setAutoBtn = document.getElementById("setAutoBtn");
    const setManualBtn = document.getElementById("setManualBtn");

    // Websockets
    const wsControl = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/control`);

    /* Websocket variables */
    let opMode = "";
    let uvMode = "";
    

    // Turn UV light on button logic
    uvOnButton.addEventListener('click', () => {
      if (wsControl.readyState !== WebSocket.OPEN) {
        alert("Cannot turn on the UV light: connection to server is not established yet.");
        return;
      }
      
      if(uvMode == "uvOn"){
        alert("Cannot turn on the UV light: the UV light has already been ON");
        return;
      } else {
        uvMode = "uvOn";
        wsControl.send("on");
        alert(`The UV light has been turned ON`);
      }
     
    });

    // Turn UV light of button logic
    uvOffButton.addEventListener('click', () => {
      if (wsControl.readyState !== WebSocket.OPEN) {
        alert("Cannot turn on the UV light: connection to server is not established yet.");
        return;
      }
      /* Display text in mode text field */
      if(uvMode == "uvOff"){
        alert("Cannot turn on the UV light: The UV light has already been OFF");
        return;
      } else {
        uvMode = "uvOff";
        wsControl.send("off");
        alert(`The UV light has been turned OFF`);
      }
      
    });

    // Set the sytem to Automatic Mode
    setAutoBtn.addEventListener('click', () => {
      if (wsControl.readyState !== WebSocket.OPEN) {
        alert("Cannot change to Automatic mode: connection to server is not established yet.");
        return;
      }

      // Send a single message over WebSocket
      if (opMode == "automated") {
        alert("Cannot change to Automatic mode: the system has already been in the Automatic mode.");
        return;
      } else {
        opMode = "automated";
        /* Send message to the server */
        wsControl.send("automated");
        /* Display text in mode text field */
        alert(`The system has been changed to Automatic mode`);
      }
    });

    // Set the sytem to Manual Mode
    setManualBtn.addEventListener('click', () => {
      if (wsControl.readyState !== WebSocket.OPEN) {
        alert("Cannot change to Manual mode: connection to server is not established yet.");
        return;
      }

      if (opMode == "manual") {
        alert("Cannot change to Manual mode: the system has already been in the Manual mode.");
        return;
      } else {
          opMode = "manual";
          // Send a single message over WebSocket
          wsControl.send("manual");
          /* Display text in mode text field */
          alert(`The system has been changed to Manual mode`);
      }
    });


    // Stop button functionality
    stopButton.addEventListener("click", function () {
        if (wsControl.readyState !== WebSocket.OPEN) {
            alert("Cannot stop: connection to server is not established yet.");
            return;
        }

        // Send a single message over WebSocket
        wsControl.send("stop");
    });

    // Modal logic
    const plantModal = document.getElementById("plantModal");
    const openModalBtn = document.getElementById("openPlantModal");
    const closeBtn = document.querySelector("#plantModal .close");

    if (plantModal && openModalBtn && closeBtn) {
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
    }

    // Create Plant
    const bed1 = document.getElementById("bed1");
    const bed2 = document.getElementById("bed2");

    for (let i = 1; i <= 8; i++) {
      const btn = document.createElement("button");
      btn.className = "plant-btn";
      btn.textContent = `Plant ${i}`;
      btn.dataset.id = i;
      btn.onclick = () => togglePlant(btn);
      bed1.appendChild(btn);
    }

    for (let i = 9; i <= 16; i++) {
      const btn = document.createElement("button");
      btn.className = "plant-btn";
      btn.textContent = `Plant ${i}`;
      btn.dataset.id = i;
      btn.onclick = () => togglePlant(btn);
      bed2.appendChild(btn);
    }
    
    function togglePlant(button) {
      const plantId = button.dataset.id;
      const isInactive = button.classList.toggle("inactive");
      const message = isInactive ? `Choose Plant ${plantId}` : `Unchoose Plant ${plantId}`;

      if (wsControl && wsControl.readyState === WebSocket.OPEN) {
        wsControl.send(message);  
        console.log(`Sent: ${message}`);
      } else {
        console.warn("WebSocket not connected.");
      }
    }

    document.getElementById("resetPlants").addEventListener("click", () => {
      const allPlantButtons = document.querySelectorAll(".plant-btn");

      allPlantButtons.forEach(btn => {
        // Only change if currently green (i.e., not already inactive)
        if (btn.classList.contains("inactive")) {
          btn.classList.toggle("inactive");
        }
      });

      if (wsControl && wsControl.readyState === WebSocket.OPEN) {
        wsControl.send("reset");
        console.log("Sent: reset");
      } else {
        console.warn("WebSocket not connected.");
      }
    });

});
