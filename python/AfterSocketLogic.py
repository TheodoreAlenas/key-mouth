class AfterSocketLogicAllUsers:

    last_id = -1
    per_socket_objects = {}

    def register(self, socket_object):
        self.last_id += 1
        self.per_socket_objects[self.last_id] = socket_object
        return self.last_id


class AfterSocketLogicSingleUser:

    timestamps = []
    actions = []
    prev_input = ''

    def __init__(self, all_users):
        self.all_users = all_users
        self.socket_id = all_users.register(self)

    def get_json(self, data, time):
        self.append_diff_to_actions(data, time)
        return actions_to_json(self.actions)

    def append_diff_to_actions(self, input_field_text, time):
        if input_field_text == "clear":
            self.prev_input = ''
            return
        new_input = input_field_text[1:]
        to_append = get_diff(self.prev_input, new_input)
        to_append["user"] = self.socket_id
        to_append["time"] = time
        self.actions.append(to_append)
        self.prev_input = new_input


def get_diff(a, b):
    if str.startswith(b, a):
        return {
            "action": "wrote",
            "body": b[len(a):],
        }
    if str.startswith(a, b):
        return {
            "action": "deleted",
            "n": len(a) - len(b) + 1,
        }
    return {
        "action": "changed",
        "prev": a,
        "next": b,
    }


def actions_to_json(actions):
    message_start = {"type": "wrote", "body": ""}
    message_groups = [[{"name": "Sotiris", "message": [message_start.copy()]}]]
    message = message_groups[0][0]["message"]
    last_action = "wrote"
    del_n = 0
    prev_time = None
    for action in actions:
        if prev_time is not None and action["time"] - prev_time > 1.0:
            message_groups.append([{"name": "Sotiris", "message": [message_start.copy()]}])
            message = message_groups[-1][0]["message"]
            last_action = "wrote"
        prev_time = action["time"]
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
    return message_groups