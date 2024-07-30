from a_feature import say_hi
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.websocket("/")
async def root(websocket: WebSocket):
    await websocket.accept()
    try:
        actions = []
        prev_input = ''
        while True:
            data = await websocket.receive_text()
            if data == "clear":
                prev_input = ''
            else:
                new_input = data[1:]
                if str.startswith(new_input, prev_input):
                    actions.append({
                        "action": "wrote",
                        "body": new_input[len(prev_input):]
                    })
                elif str.startswith(prev_input, new_input):
                    actions.append({
                        "action": "deleted",
                        "n": len(prev_input) - len(new_input) + 1
                    })
                else:
                    actions.append({
                        "action": "changed",
                        "prev": prev_input,
                        "new": new_input
                    })
                prev_input = new_input
            await websocket.send_json(actions_to_json(actions))
    except WebSocketDisconnect as e:
        pass


def actions_to_json(actions):
    message = [{"type": "wrote", "body": ""}]
    last_action = "wrote"
    del_n = 0
    for action in actions:
        if action["action"] == "wrote":
            if last_action == "wrote":
                message[-1]["body"] += action["body"]
            else:
                message.append({
                    "type": "wrote",
                    "body": action["body"]
                })
        elif action["action"] == "deleted":
            if last_action == "deleted":
                message[-1]["body"] = message[-2]["body"][-(action["n"] - 1):] + message[-1]["body"]
                message[-2]["body"] = message[-2]["body"][:-(action["n"] - 1)]
                del_n += action["n"]
            else:
                message.append({
                    "type": "deleted",
                    "body": message[-1]["body"][-(action["n"] - 1):]
                })
                message[-2]["body"] = message[-2]["body"][:-(action["n"] - 1)]
                del_n = action["n"]
        else:
            message.append({
                "type": "wrote",
                "body": "<unhandled>"
            })
        last_action = action["action"]
    return [{
        "name": "Sotiris",
        "message": message
    }]
