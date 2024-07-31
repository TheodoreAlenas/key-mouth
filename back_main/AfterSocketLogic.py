from back_main.InputFieldDiffGenerator import InputFieldDiffGenerator


class AfterSocketLogic:

    input_field_diff_generator = InputFieldDiffGenerator()

    def get_json(self, data, time):
        actions = self.input_field_diff_generator.get(data, time)
        return actions_to_json(actions)


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
