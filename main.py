from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from typing import Dict, Set
from fastapi.websockets import WebSocketDisconnect 
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 部屋ごとのWebSocket接続を管理
room_websockets: Dict[str, Set[WebSocket]] = {}

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()

    if room_name not in room_websockets:
        room_websockets[room_name] = set()
        
    room_websockets[room_name].add(websocket)
    print(room_websockets)

    #メッセージのやり取り、退出判定
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            print(data)

            userName = data.get("userName", "Unknown User")
            message = data.get("message", "")
            
            response_data = {
                "userName": userName,
                "message": message
            }
            for ws in room_websockets.get(room_name, []):
                await ws.send_text(json.dumps(response_data))
                
    except WebSocketDisconnect:
        room_websockets[room_name].remove(websocket)
        if not room_websockets[room_name]:
            del room_websockets[room_name]
            print(room_websockets)
