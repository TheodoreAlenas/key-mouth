from AfterSocketLogic import AfterSocketLogic, Moments
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from time import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_items = [
    [
        {"connId": 4, "type": "write", "body": "H"},
        {"connId": 4, "type": "write", "body": "i"},
        {"connId": 4, "type": "write", "body": " Mst"},
        {"connId": 4, "type": "delete", "body": "s"},
        {"connId": 4, "type": "delete", "body": "t"},
        {"connId": 4, "type": "write", "body": "ark"}
    ],
    [
        {"connId": 4, "type": "write", "body": "Are you there?"},
        {"connId": 5, "type": "write",
         "body": "I thought I'd find you here"}
    ]
]


@app.get("/last")
async def root():
    return fake_items


logic = AfterSocketLogic(Moments())
id_to_sock = {}
async def send_jsons(to_send):
    for conn, json in to_send:
        await id_to_sock[conn].send_json(json)

@app.websocket("/")
async def root(websocket: WebSocket):
    conn_id = None
    try:
        await websocket.accept()
        metadata = await websocket.receive_json()
        if metadata["version"] != 0:
            print("Error: the client uses an unsupported version: "
                  + str(metadata["version"]))
            websocket.close(code=1002, reason="only v0 is supported")
            return
        to_send, conn_id = logic.register(time())
        await send_jsons(to_send)
        id_to_sock[conn_id] = websocket
        while True:
            data = await websocket.receive_text()
            to_send = logic.handle_input(time(), conn_id, data)
            await send_jsons(to_send)
    except WebSocketDisconnect as e:
        id_to_sock.pop(conn_id)
        to_send = logic.disconnect(time(), conn_id)
        await send_jsons(to_send)
