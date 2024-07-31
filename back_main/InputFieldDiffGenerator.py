class InputFieldDiffGenerator:

    actions = []
    prev_input = ''

    def get(self, data, time):
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
        return self.actions
