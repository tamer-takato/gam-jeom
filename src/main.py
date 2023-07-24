# main.py
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from scoring_system import Match
from joystick import Joystick
from phone import Phone
from display import Display
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
mysql = MySQL(app)

match = Match(match_number=1, category="Male", criteria="points", point_gap=10, round_time=120, rest_time=30)
joysticks = [Joystick(joystick_id) for joystick_id in range(1, 6)]
phones = [Phone(phone_id) for phone_id in range(1,6)]
display = Display()

def add_player_to_database(name, nationality):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO players (name, nationality) VALUES (%s, %s)", (name, nationality))
    mysql.connection.commit()
    cur.close()

def add_match_to_database(match_number, category, criteria, point_gap, round_time, rest_time):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO matches (match_number, category, criteria, point_gap, round_time, rest_time) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (match_number, category, criteria, point_gap, round_time, rest_time))
    mysql.connection.commit()
    cur.close()

@app.route('/start_match', methods=['POST'])
def start_match():
    data = request.get_json()
    blue_player_name = data['blue_player_name']
    blue_player_nationality = data['blue_player_nationality']
    red_player_name = data['red_player_name']
    red_player_nationality = data['red_player_nationality']
    judges_count = data['judges_count']

    # Add players to the database
    add_player_to_database(blue_player_name, blue_player_nationality)
    add_player_to_database(red_player_name, red_player_nationality)

    # Add match details to the database
    add_match_to_database(match.match_number, match.category, match.criteria,
                          match.point_gap, match.round_time, match.rest_time)

    if not match.start_match(blue_player_name, blue_player_nationality, red_player_name, red_player_nationality, judges_count):
        return jsonify({'message': 'Match cannot start without at least two judges.'}), 400

    # match.start_match(blue_player_name, blue_player_nationality, red_player_name, red_player_nationality)
    display.update_display(match)  # Update display information

    return jsonify({'message': 'Match started successfully!'})

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.get_json()
    player = data['player']
    points = data['points']

    match.add_score(player, points)

    if match.criteria == 'rounds':
        # Add the round winner to rounds
        winner = 'blue' if player == 'blue' else 'red'
        match.add_round_score(winner)

    display.update_display(match)  # Update display information

    return jsonify({'message': 'Score added successfully!'})

@app.route('/add_penalty', methods=['POST'])
def add_penalty():
    data = request.get_json()
    player = data['player']

    match.add_penalty(player)
    display.update_display(match)  # Update display information

    return jsonify({'message': 'Penalty added successfully!'})

@app.route('/check_match_outcome', methods=['GET'])
def check_match_outcome():
    outcome = match.check_match_outcome()

    return jsonify({'outcome': outcome})

@app.route('/assign_buttons', methods=['POST'])
def assign_buttons():
    data = request.get_json()
    joystick_id = data['joystick_id']
    player = data['player']
    buttons = data['buttons']

    joystick = joysticks[joystick_id - 1]
    for button_name, points in buttons.items():
        joystick.assign_button(button_name, player, points)

    return jsonify({'message': 'Buttons assigned successfully!'})

@app.route('/handle_joystick_input', methods=['POST'])
def handle_joystick_input():
    data = request.get_json()
    joystick_id = data['joystick_id']
    buttons_pressed = data['buttons_pressed']

    joystick = joysticks[joystick_id - 1]

    blue_points = 0
    red_points = 0

    for button_name in buttons_pressed:
        if button_name.startswith('blue_button'):
            blue_points += joystick.handle_input(button_name)
        elif button_name.startswith('red_button'):
            red_points += joystick.handle_input(button_name)

    match.add_score('blue', blue_points)
    match.add_score('red', red_points)

    return jsonify({'message': 'Joystick input handled successfully!'})

@app.route('/set_phone_key', methods=['POST'])
def set_phone_key():
    data = request.get_json()
    phone_id = data['phone_id']
    key = data['key']

    phone = phones[phone_id - 1]
    phone.set_key(key)

    return jsonify({'message': 'Phone key set successfully!'})

@app.route('/handle_phone_input', methods=['POST'])
def handle_phone_input():
    data = request.get_json()
    phone_id = data['phone_id']
    button_name = data['button_name']

    phone = phones[phone_id - 1]
    player, points = phone.handle_input(button_name)

    if player:
        match.add_score(player, points)

    return jsonify({'message': 'Phone input handled successfully!'})

@app.route('/set_video_replay_available', methods=['POST'])
def set_video_replay_available():
    data = request.get_json()
    player = data['player']
    availability = data['availability']

    if player == 'blue':
        match.blue_player.set_video_replay_available(availability)
    elif player == 'red':
        match.red_player.set_video_replay_available(availability)

    display.update_display(match)  # Update display information
    return jsonify({'message': 'Video replay availability set successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
