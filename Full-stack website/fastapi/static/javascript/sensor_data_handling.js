document.addEventListener("DOMContentLoaded", function () {
    const wsData = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/data`);

    wsData.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);

            if (data.battery_value !== undefined) {
                document.getElementById("batteryData").textContent = `${data.battery_value} %`;
            }

            if (data.speed_value !== undefined) {
                document.getElementById("speedData").textContent = `${data.speed_value.toFixed(1)} m/s`;
            }

            if (data.power_value !== undefined) {
                document.getElementById("powerData").textContent = `${data.power_value} W`;
            }

        } catch (e) {
            console.error("Invalid JSON data:", event.data);
        }
    };
});
