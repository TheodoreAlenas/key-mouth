class AfterSocketLogic:

    actions = []
    prev_input = ''

    def get_json_from_data(self, data):
        self.diff_new_data(data)
        return actions_to_json(self.actions)

    def diff_new_data(self, data):
        if data == "clear":
            self.prev_input = ''
            return
        new_input = data[1:]
        if str.startswith(new_input, self.prev_input):
            self.actions.append({
                "action": "wrote",
                "body": new_input[len(self.prev_input):]
            })
        elif str.startswith(self.prev_input, new_input):
            self.actions.append({
                "action": "deleted",
                "n": len(self.prev_input) - len(new_input) + 1
            })
        else:
            self.actions.append({
                "action": "changed",
                "prev": self.prev_input,
                "new": new_input
            })
        self.prev_input = new_input


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
