import asyncio
import websockets
import random 
import json
from pydantic import BaseModel

# Hardcoded WebSocket settings
# PUBLIC TEST
HOST = "episode-purse-clock-guilty.trycloudflare.com"
PORT = "443"
SECURE = True
SCHEME = "wss" if SECURE else "ws"

# LOCAL TEST
# HOST = "127.0.0.1"     
# PORT = "8000"
# SECURE = False      
# SCHEME = "wss" if SECURE else "ws"


# Receive-only endpoints
RECEIVE_PATHS = ["/ws/directions", "/ws/control"]
# Send-only endpoint
SEND_PATH = "/ws/data"

class SensorData(BaseModel):
    speed_value: float = 0
    power_value: float = 0
    battery_value: int = 0

def make_url(path):
    if (SECURE and PORT == "443") or (not SECURE and PORT == "80"):
        return f"{SCHEME}://{HOST}{path}"
    else:
        return f"{SCHEME}://{HOST}:{PORT}{path}"

RECEIVE_URLS = [make_url(p) for p in RECEIVE_PATHS]
SEND_URL = make_url(SEND_PATH)

# --- Receiving logic ---
async def receive_only(url):
    while True:
        try:
            print(f"[{url}] Attempting to connect for receiving...")
            async with websockets.connect(url) as websocket:
                print(f"[{url}] Connected.")
                while True:
                    message = await websocket.recv()
                    print(f"[{url}] Received: {message}")
        except Exception as e:
            print(f"[{url}] Receive error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

# --- Sending logic ---
async def send_only(url):
    while True:
        try:
            print(f"[{url}] Attempting to connect for sending...")
            async with websockets.connect(url) as websocket:
                print(f"[{url}] Connected.")
                while True:
                    # Replace input() with any sensor reading or looped message
                    data = SensorData(
                        speed_value=round(random.uniform(0, 1.5), 2),
                        power_value=round(random.uniform(0, 150), 1),
                        battery_value=random.randint(0, 100)
                    )
                    json_data = data.model_dump_json()
                    await websocket.send(json_data)
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"[{url}] Send error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

# --- Main runner ---
async def main():
    tasks = []
    # Launch all receive endpoints
    for url in RECEIVE_URLS:
        tasks.append(asyncio.create_task(receive_only(url)))
    # Launch the send endpoint
    tasks.append(asyncio.create_task(send_only(SEND_URL)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
