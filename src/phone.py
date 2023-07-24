# phone.py

class Phone:
    def __init__(self, phone_id):
        self.phone_id = phone_id
        self.key = None
        self.button_mapping = {
            'button1': None,
            'button2': None,
            'button3': None,
            'button4': None
        }

    def assign_button(self, button_name, player, points):
        self.button_mapping[button_name] = (player, points)

    def set_key(self, key):
        self.key = key

    def handle_input(self, button_name):
        if button_name in self.button_mapping:
            player, points = self.button_mapping[button_name]
            return player, points
        return None, 0
