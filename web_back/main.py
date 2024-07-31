from back_main import AfterSocketLogic
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.websocket("/")
async def root(websocket: WebSocket):
    after_socket_logic = AfterSocketLogic()
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            json = after_socket_logic.get_json_from_data(data)
            await websocket.send_json(json)
    except WebSocketDisconnect as e:
        pass
