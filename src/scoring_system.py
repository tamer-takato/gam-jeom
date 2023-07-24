# scoring_system.py

class Player:
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality
        self.score = 0
        self.penalties = 0
	self.video_replay_available = True # per WT Rules, player will always have Video Replay Quota enabled.

    def set_video_replay_available(self, availability):
        self.video_replay_available = availability

class Match:
    def __init__(self, event_id, event_name, match_number, category, criteria, point_gap, round_time, rest_time):
	self.event_id = event_id
	self.event_name = event_name
        self.match_number = match_number
        self.category = category
        self.criteria = criteria
        self.point_gap = point_gap
        self.round_time = round_time
        self.rest_time = rest_time
        self.blue_player = None
        self.red_player = None
        self.match_in_progress = False
        self.rounds = []  # List to store scores for each round

    def start_match(self, blue_player_name, blue_player_nationality, red_player_name, red_player_nationality, judges_count):
        if judges_count < 2:
            return False  # Match cannot start without at least two judges
        self.blue_player = Player(blue_player_name, blue_player_nationality)
        self.red_player = Player(red_player_name, red_player_nationality)
        self.match_in_progress = True
        self.rounds = []  # Reset rounds for a new match
        return True

    def add_score(self, player, points):
        if player == 'blue':
            self.blue_player.score += points
        elif player == 'red':
            self.red_player.score += points

    def del_score(self, player, points):
	if player == 'blue':
	    self.blue_player.score -= points
	elif player == 'red':
	    self.red_player.score -= points

    def add_penalty(self, player):
        if player == 'blue':
            self.blue_player.penalties += 1
	    self.red_player.score += 1
        elif player == 'red':
            self.red_player.penalties += 1
	    self.blue_player.score += 1

    def del_penalty(self, player):
        if player == 'blue':
            self.blue_player.penalties -= 1
            self.red_player.score -= 1
        elif player == 'red':
            self.red_player.penalties -= 1
            self.blue_player.score -= 1

    def add_round_score(self, winner):
        self.rounds.append(winner)

    def determine_match_winner_by_rounds(self):
        if self.rounds.count('blue') >= 2:
            return 'blue'
        elif self.rounds.count('red') >= 2:
            return 'red'
        return None

    def determine_match_winner(self):
        if self.criteria == 'points':
            return self.determine_match_winner_by_points()
        elif self.criteria == 'rounds':
            return self.determine_match_winner_by_rounds()

    def determine_match_winner_by_points(self):
        if abs(self.blue_player.score - self.red_player.score) >= self.point_gap:
            return 'blue' if self.blue_player.score > self.red_player.score else 'red'
        return None

    def determine_match_winner_by_rounds(self):
        if self.rounds.count('blue') >= 2:
            return 'blue'
        elif self.rounds.count('red') >= 2:
            return 'red'
        return None

    def check_match_outcome(self):
        if self.criteria == 'points':
            return self.check_by_points()
        elif self.criteria == 'rounds':
            return self.check_by_rounds()

    def check_by_points(self):
        if abs(self.blue_player.score - self.red_player.score) >= self.point_gap:
            self.match_in_progress = False
            return 'blue' if self.blue_player.score > self.red_player.score else 'red'
        return None

    def check_by_rounds(self):
        # Logic for determining match outcome based on rounds
        pass
