# joystick.py

class Joystick:
    def __init__(self, joystick_id):
        self.joystick_id = joystick_id
        self.button_mapping = {
            'blue_button1': None,
            'blue_button2': None,
            'blue_button3': None,
            'blue_button4': None,
            'red_button1': None,
            'red_button2': None,
            'red_button3': None,
            'red_button4': None
        }

    def assign_button(self, button_name, player, points):
        if player == 'blue':
            if button_name.startswith('blue_button'):
                self.button_mapping[button_name] = points
        elif player == 'red':
            if button_name.startswith('red_button'):
                self.button_mapping[button_name] = points

    def handle_input(self, button_name):
        points = self.button_mapping.get(button_name, 0)
        return points
