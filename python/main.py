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
id_to_sock = {}
mutex = threading.Lock()
logic = AfterSocketLogic(time=time(),
                         moments_db=Moments(time()),
                         min_silence=1.0,
                         min_moment=0.5)


@app.get("/last")
async def last():
    return logic.get_last_few()


async def wrap(f, args):
    mutex.acquire()
    to_send, to_return = f(time(), args)
    mutex.release()
    for conn, json in to_send:
        await id_to_sock[conn].send_json(json)
    return to_return


@app.websocket("/")
async def root(websocket: WebSocket, session: str):
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
        if conn_id is not None:
            id_to_sock.pop(conn_id)
            await wrap(logic.disconnect, conn_id)
