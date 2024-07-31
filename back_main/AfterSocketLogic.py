from back_main.InputFieldDiffGenerator import InputFieldDiffGenerator


class AfterSocketLogic:

    input_field_diff_generator = InputFieldDiffGenerator()

    def get_json(self, data, time):
        actions = self.input_field_diff_generator.get(data, "Sotiris", time)
        return actions_to_json(actions)


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
