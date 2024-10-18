
# License at the bottom

from wiring.Main import Main
from lib.exceptions import LogicHttpException
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import typing
from time import time
import threading
from os import environ

moments_per_page = 50
min_silence = 3.0
min_moment = 1.0

a = 'KEYMOUTH_MOMENTS_PER_PAGE'
if a in environ:
    moments_per_page = int(environ[a])
    assert moments_per_page > 0, f"{a} is set, but it's {environ[a]}"

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

app = fastapi.FastAPI()
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
def create_logic(min_silence, min_moment):
    return Main(
        time=time(),
        db=db_only_use_in_inttest_and_logic_init,
        min_silence=min_silence,
        min_moment=min_moment,
        moments_per_page=moments_per_page
    )
logic = create_logic(min_silence=min_silence, min_moment=min_moment)
if inttest is not None:
    logic = inttest.add_room_and_restart(logic, create_logic)
a = 'KEYMOUTH_ADD_A_ROOM'
if a in environ and environ[a] == 'yes':
    logic.create_room(time(), 'empty-room')
    logic.rename_room(time(), ('empty-room', 'Empty Room'))
    logic.create_room(0.0, 'filled-room')
    logic.rename_room(0.1, ('filled-room', 'Filled Room'))
    _, conn = logic.connect(0.2, 'filled-room')
    for i in range(1, 20):
        conn.handle_input(10.0 * i, f'+{i}')


def do_nothing(_):
    pass


async def wrap(f, args, before_sending=do_nothing):
    mutex.acquire()
    try:
        if inttest is not None:
            inttest.raise_exception_once('before releasing mutex')
        to_send, to_return = f(time(), args)
        mutex.release()
        before_sending(to_return)
        for conn, json in to_send:
            try:
                await id_to_sock[conn].send_json(json)
            except Exception:
                pass
        return to_return
    except LogicHttpException as e:
        if mutex.locked():
            mutex.release()
        raise fastapi.HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        if mutex.locked():
            mutex.release()
        raise e
    if mutex.locked():
        mutex.release()


@app.get("/")
async def root_get():
    return await wrap(logic.get_rooms, None)


@app.put("/{room}")
async def room_put(room: str):
    await wrap(logic.create_room, room)


@app.put("/{room}/name/{name}")
async def room_name_put(room: str, name: str):
    await wrap(logic.rename_room, (room, name))


@app.delete("/{room}")
async def room_delete(room: str):
    await wrap(logic.delete_room, room)


@app.get("/{room}")
async def room_get(
        room: str,
        start: typing.Annotated[
            int,
            fastapi.Query(title="inclusive", ge=0)
        ],
        end: typing.Annotated[
            int,
            fastapi.Query(title="exclusive and not guaranteed", ge=1)
        ]
):
    return await wrap(logic.get_pages_range, (room, start, end))


@app.websocket("/{room}")
async def root(websocket: fastapi.WebSocket, room: str):
    logic.if_room_is_missing_throw(room)
    conn = None
    try:
        await websocket.accept()
        metadata = await websocket.receive_json()
        if metadata["version"] != "0.2.0":
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
    except fastapi.WebSocketDisconnect as e:
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
