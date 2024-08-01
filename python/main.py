from AfterSocketLogic import AfterSocketLogic
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from time import time

app = FastAPI()
logic = AfterSocketLogic()

@app.websocket("/")
async def root(websocket: WebSocket):
    try:
        await websocket.accept()
        metadata = await websocket.receive_json()
        if metadata["version"] != 0:
            print("Error: the client uses an unsupported version: "
                  + str(metadata["version"]))
            websocket.close(code=1002, reason="only v0 is supported")
            return
        conn_id = logic.register(time())
        while True:
            data = await websocket.receive_text()
            json = logic.get_json(data, time())
            await websocket.send_json(json)
    except WebSocketDisconnect as e:
        pass
