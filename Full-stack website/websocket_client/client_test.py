import asyncio
import websockets
from pydantic import BaseModel

# 🔒 Hardcoded values for Cloudflare Tunnel
# HOST = "horse-un-peripherals-gifts.trycloudflare.com"
HOST = "127.0.0.1"
PORT = "443"
SECURE = True

SCHEME = "wss" if SECURE else "ws"

PATHS = [
    "/ws/directions",
    "/ws/control"
]

class SensorData(BaseModel):
    speed_value: float = 0
    power_value: float = 0
    battery_value: int = 0

def make_url(path):
    if (SECURE and PORT == "443") or (not SECURE and PORT == "80"):
        return f"{SCHEME}://{HOST}{path}"
    else:
        return f"{SCHEME}://{HOST}:{PORT}{path}"

ENDPOINTS = [make_url(path) for path in PATHS]

async def listen_to_endpoint(url):
    while True:
        try:
            print(f"[{url}] Attempting to connect...")
            async with websockets.connect(url) as websocket:
                print(f"[{url}] Connected.")
                while True:
                    message = await websocket.recv()
                    print(f"[{url}] Received: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"[{url}] Connection closed: {e}. Reconnecting in 5 seconds...")
        except Exception as e:
            print(f"[{url}] Error: {e}. Reconnecting in 5 seconds...")
        await asyncio.sleep(5)

async def main():
    tasks = [asyncio.create_task(listen_to_endpoint(url)) for url in ENDPOINTS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
