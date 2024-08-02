from AfterSocketLogic import AfterSocketLogic, Moments
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from time import time
import threading

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


id_to_sock = {}

logic = AfterSocketLogic(time(), Moments(time()), 1.0, 0.5)
mutex = threading.Lock()


async def wrap(f, args):
    mutex.acquire()
    to_send, to_return = f(time(), args)
    mutex.release()
    for conn, json in to_send:
        await id_to_sock[conn].send_json(json)
    return to_return


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
        conn_id = await wrap(logic.register, None)
        id_to_sock[conn_id] = websocket
        while True:
            data = await websocket.receive_text()
            await wrap(logic.handle_input, (conn_id, data))
    except WebSocketDisconnect as e:
        id_to_sock.pop(conn_id)
        await wrap(logic.disconnect, conn_id)
