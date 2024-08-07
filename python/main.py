from AfterSocketLogic import AfterSocketLogic, AfterSocketPublicLogic, Conn, Moments, LogicHttpException
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
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
id_to_sock = {}
mutex = threading.Lock()
DONT_USE_THIS = AfterSocketLogic(time=time(),
                                 moments_db=Moments(time()),
                                 min_silence=1.0,
                                 min_moment=0.5)
logic = AfterSocketPublicLogic(DONT_USE_THIS)
logic.create_room(time(), "0")
logic.create_room(time(), "hello")


async def wrap(f, args):
    mutex.acquire()
    try:
        to_send, to_return = f(time(), args)
        mutex.release()
        for conn, json in to_send:
            await id_to_sock[conn].send_json(json)
        return to_return
    except LogicHttpException as e:
        mutex.release()
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.put("/room")
async def create_room(room: str):
    await wrap(logic.create_room, room)


@app.get("/last")
async def last(room: str):
    return await wrap(logic.get_last_few, room)


@app.websocket("/")
async def root(websocket: WebSocket, room: str):
    conn_id = None
    try:
        await websocket.accept()
        metadata = await websocket.receive_json()
        if metadata["version"] != 0:
            print("Error: the client uses an unsupported version: "
                  + str(metadata["version"]))
            websocket.close(code=1002, reason="only v0 is supported")
            return
        conn_id = await wrap(logic.connect, room)
        id_to_sock[conn_id] = websocket
        while True:
            data = await websocket.receive_text()
            await wrap(DONT_USE_THIS.handle_input, (conn_id, data))
    except WebSocketDisconnect as e:
        if conn_id is not None:
            id_to_sock.pop(conn_id)
            await wrap(DONT_USE_THIS.disconnect, conn_id)
