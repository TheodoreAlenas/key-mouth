class InputFieldDiffGenerator:

    actions = []
    prev_input = ''

    def get(self, input_field_text, user, time):
        self.mutate(input_field_text, user, time)
        return self.actions

    def mutate(self, input_field_text, user, time):
        if input_field_text == "clear":
            self.prev_input = ''
            return
        new_input = input_field_text[1:]
        if str.startswith(new_input, self.prev_input):
            self.actions.append({
                "action": "wrote",
                "body": new_input[len(self.prev_input):],
                "time": time
            })
        elif str.startswith(self.prev_input, new_input):
            self.actions.append({
                "action": "deleted",
                "n": len(self.prev_input) - len(new_input) + 1,
                "time": time
            })
        else:
            self.actions.append({
                "action": "changed",
                "prev": self.prev_input,
                "new": new_input,
                "time": time
            })
        self.prev_input = new_input
