from AfterSocketLogic import AfterSocketLogic, Moments
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from time import time

app = FastAPI()
logic = AfterSocketLogic(Moments())

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
