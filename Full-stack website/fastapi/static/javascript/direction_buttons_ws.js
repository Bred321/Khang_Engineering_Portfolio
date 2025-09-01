document.addEventListener("DOMContentLoaded", function () {
    // var ws_forward = new WebSocket("ws://localhost:8000/ws/forward");
    // var ws_backward = new WebSocket("ws://localhost:8000/ws/backward");
    // var ws_right = new WebSocket("ws://localhost:8000/ws/right");
    // var ws_left = new WebSocket("ws://localhost:8000/ws/left");

    const wsDirections = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/directions`);

    // Websocket endpoint handling function
    function registerControlButton(buttonSelector, websocket, message) {
        const btn = document.getElementById(buttonSelector);
        let isPressed = false;

        const startSending = () => {
            if (!isPressed) {
                websocket.send(message);
                isPressed = true;
            }
        };

        const stopSending = () => {
            if (isPressed) {
                websocket.send("stop");
                isPressed = false;
            }
        };

        // Mouse events
        btn.addEventListener("mousedown", startSending);
        btn.addEventListener("mouseup", stopSending);
        btn.addEventListener("mouseleave", stopSending);

        // Touch events
        btn.addEventListener("touchstart", startSending);
        btn.addEventListener("touchend", stopSending);
        btn.addEventListener("touchcancel", stopSending);
    }

    wsDirections.onopen = () => {
        registerControlButton("forwardBtn", wsDirections, "forward");
        registerControlButton("backwardBtn", wsDirections, "backward");
        registerControlButton("leftBtn", wsDirections, "left");
        registerControlButton("rightBtn", wsDirections, "right");
    };
});