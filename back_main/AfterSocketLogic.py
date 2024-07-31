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
        if str.startswith(new_input, self.prev_input):
            self.actions.append({
                "user": self.socket_id,
                "time": time,
                "action": "wrote",
                "body": new_input[len(self.prev_input):],
            })
        elif str.startswith(self.prev_input, new_input):
            self.actions.append({
                "user": self.socket_id,
                "time": time,
                "action": "deleted",
                "n": len(self.prev_input) - len(new_input) + 1,
            })
        else:
            self.actions.append({
                "user": self.socket_id,
                "time": time,
                "action": "changed",
                "prev": self.prev_input,
                "new": new_input,
            })
        self.prev_input = new_input


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
