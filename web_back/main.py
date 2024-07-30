from a_feature import say_hi
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.websocket("/")
async def root(websocket: WebSocket):
    await websocket.accept()
    try:
        prevInput = ""
        while True:
            data = await websocket.receive_text()
            if str.startswith(data, prevInput):
                prevInput = data
            elif str.startswith(prevInput, data):
                prevInput = data + "[deleted]"
            else:
                prevInput = "[new]" + data
            await websocket.send_json([{"name": "Sotiris", "message": [prevInput]}])
    except WebSocketDisconnect as e:
        pass
