from back_main.AfterSocketLogic import AfterSocketLogicSingleUser, AfterSocketLogicAllUsers
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from time import time

app = FastAPI()
logic_all_users = AfterSocketLogicAllUsers()

@app.websocket("/")
async def root(websocket: WebSocket):
    logic = AfterSocketLogicSingleUser(logic_all_users)
    await websocket.accept()
    try:
        metadata = await websocket.receive_json()
        if metadata["version"] != 0:
            print("Error: the client uses an unsupported version: "
                  + str(metadata["version"]))
            websocket.close(code=1002, reason="only v0 is supported")
        while True:
            data = await websocket.receive_text()
            json = logic.get_json(data, time())
            await websocket.send_json(json)
    except WebSocketDisconnect as e:
        pass
