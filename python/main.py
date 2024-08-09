
# License at the bottom

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


@app.get("/")
async def root_get():
    return await wrap(logic.get_rooms, None)


@app.put("/{room}")
async def room_put(room: str):
    await wrap(logic.create_room, room)


@app.get("/{room}")
async def room_get(room: str,
                   start: int|None = None,
                   end: int|None = None):
    return await wrap(logic.get_moments_range, (room, start, end))


@app.websocket("/{room}")
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


'''
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
