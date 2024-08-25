
# License at the bottom

from AfterSocketLogic import AfterSocketLogic, LogicHttpException, ConfTiming
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from time import time
import threading
from os import environ

a = 'KEYMOUTH_RAM_DB'
if a in environ and environ[a] == 'yes':
    from db.mock import Db
else:
    from db.mongo import Db

inttest = None
a = 'KEYMOUTH_INTTEST_WIDGETS'
if a in environ and environ[a] == 'yes':
    from IntTestWidgets import IntTestWidgets
    inttest = IntTestWidgets()

app = FastAPI()
a = 'KEYMOUTH_CORS_ALL'
if a in environ and environ[a] == 'yes':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
id_to_sock = {}
mutex = threading.Lock()
db_only_use_in_inttest_and_logic_init = Db()
def create_logic():
    return AfterSocketLogic(
        time=time(),
        db=db_only_use_in_inttest_and_logic_init,
        conf_timing=ConfTiming(
            min_silence=3.0,
            min_moment=1.0
        ))
logic = create_logic()
if inttest is not None:
    logic = inttest.add_room_and_restart(
        logic, db_only_use_in_inttest_and_logic_init)
a = 'KEYMOUTH_ADD_A_ROOM'
if a in environ and environ[a] == 'yes':
    logic.create_room(time(), 'test-room')
    logic.rename_room(time(), ('test-room', 'Test Room'))


def do_nothing(_):
    pass


async def wrap(f, args, before_sending=do_nothing):
    mutex.acquire()
    released_the_mutex = False
    try:
        if inttest is not None:
            inttest.raise_exception_once('before releasing mutex')
        to_send, to_return = f(time(), args)
        mutex.release()
        released_the_mutex = True
        before_sending(to_return)
        for conn, json in to_send:
            try:
                await id_to_sock[conn].send_json(json)
            except Exception:
                pass
        return to_return
    except LogicHttpException as e:
        if not released_the_mutex:
            mutex.release()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        if not released_the_mutex:
            mutex.release()
        raise e
    if not released_the_mutex:
        mutex.release()


@app.get("/")
async def root_get():
    return await wrap(logic.get_rooms, None)


@app.put("/{room}")
async def room_put(room: str):
    await wrap(logic.create_room, room)


@app.put("/{room_id}/name/{name}")
async def room_name_post(room_id: str, name: str):
    await wrap(logic.rename_room, (room_id, name))


@app.delete("/{room}")
async def room_delete(room: str):
    await wrap(logic.delete_room, room)


@app.get("/{room}")
async def room_get(room: str, start: int, end: int):
    return await wrap(logic.get_moments_range, (room, start, end))


@app.websocket("/{room}")
async def root(websocket: WebSocket, room: str):
    if not room in logic.rooms_ram:
        raise HTTPException(status_code=404, detail="room missing")
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
        conn = await wrap(logic.connect, room,
                          before_sending=assign_the_socket)
        while True:
            data = await websocket.receive_text()
            await wrap(conn.handle_input, data)
    except WebSocketDisconnect as e:
        if conn is not None:
            id_to_sock.pop(conn.conn_id)
            await wrap(conn.disconnect, None)


@app.on_event("shutdown")
async def on_shutdown():
    await wrap(logic.close, None)


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
