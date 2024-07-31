from back_main.AfterSocketLogic import AfterSocketLogic
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from time import time

app = FastAPI()

@app.websocket("/")
async def root(websocket: WebSocket):
    after_socket_logic = AfterSocketLogic()
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            json = after_socket_logic.get_json(data, time())
            await websocket.send_json(json)
    except WebSocketDisconnect as e:
        pass
