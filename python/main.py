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
logic = AfterSocketPublicLogic(AfterSocketLogic(
    time=time(),
    moments_db=Moments(time()),
    min_silence=1.0,
    min_moment=0.5))
logic.create_room(time(), "0")
logic.create_room(time(), "hello")


def do_nothing(_):
    pass


async def wrap(f, args, before_sending=do_nothing):
    mutex.acquire()
    try:
        to_send, to_return = f(time(), args)
        mutex.release()
        before_sending(to_return)
        for conn, json in to_send:
            await id_to_sock[conn].send_json(json)
        return to_return
    except LogicHttpException as e:
        mutex.release()
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.put("/room")
async def create_room(name: str):
    await wrap(logic.create_room, name)


@app.get("/last")
async def last(room: str):
    return await wrap(logic.get_last_few, room)


@app.websocket("/")
async def root(websocket: WebSocket, room: str):
    conn = None
    try:
        await websocket.accept()
        metadata = await websocket.receive_json()
        if metadata["version"] != 0:
            print("Error: the client uses an unsupported version: "
                  + str(metadata["version"]))
            websocket.close(code=1002, reason="only v0 is supported")
            return
        def assign_the_socket(conn):
            id_to_sock[conn.conn_id] = websocket
        conn = await wrap(logic.connect, room, assign_the_socket)
        while True:
            data = await websocket.receive_text()
            await wrap(conn.handle_input, data)
    except WebSocketDisconnect as e:
        if conn is not None:
            id_to_sock.pop(conn.conn_id)
            await wrap(conn.disconnect, None)
