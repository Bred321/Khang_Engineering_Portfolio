from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import List, Dict
from pydantic import BaseModel


# To use the fastapi command, please install "fastapi[standard]"
# A list to store all connected Python clients
class SensorData(BaseModel):
    speed_value: float = 0
    power_value: float = 0
    battery_value: int = 0
    
clients: Dict[str, List[WebSocket]] = {
    "directions": [],
    "control": [],
    "data": []
}


# Create FastAPI app and mount static files and templates
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "AGV Control Interface"})


# Websocket endpoint handling
async def handle_websocket(websocket: WebSocket, group_name: str):
    await websocket.accept()
    clients[group_name].append(websocket)
    print(f"[{group_name}]:  New client connected.")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[{group_name}]: Received from client: {data}")
            for client in clients[group_name]:
                if client != websocket:
                    await client.send_text(data)
    except Exception as e:
        print(f"[{group_name}]: Error: {e}")
    finally:
        clients[group_name].remove(websocket)
        print(f"[{group_name}]: Client disconnected. Remaining clients: {len(clients[group_name])}")
        
        
@app.websocket("/ws/directions")
async def websocket_directions(websocket: WebSocket):
    await handle_websocket(websocket, "directions")


@app.websocket("/ws/control")
async def control_button_endpoint(websocket: WebSocket):
    await handle_websocket(websocket, "control")
    
    
@app.websocket("/ws/data")
async def websocket_data_input(websocket: WebSocket):
    await websocket.accept()
    clients["data"].append(websocket)
    print("[data]: Frontend or sensor client connected.")

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data = SensorData.model_validate_json(raw_data)
                print(f"[data]: Received SensorData: {data}")

                # Broadcast the received data to all other frontend clients
                for client in clients["data"]:
                    if client != websocket:
                        await client.send_text(data.model_dump_json())

            except Exception as e:
                print(f"[data]: Invalid data format: {raw_data} ({e})")

    except Exception as e:
        print(f"[data]: Disconnected: {e}")

    finally:
        clients["data"].remove(websocket)
        print("[data]: Client removed.")

        
if __name__ == "__main__":
    # Run by command: fastapi dev app.py
    # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    # For realistic production testing: uvicorn app:app --host 0.0.0.0 --port 8000
    # For production: gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --workers 1
    # uvicorn main:app reload
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app)
