# display.py

class Display:
    def __init__(self):
        # Initialize display-related variables
        self.remaining_time = 0
        self.blue_player_score = 0
        self.red_player_score = 0
        self.blue_player_penalties = 0
        self.red_player_penalties = 0
        self.blue_player_video_replay_available = True
        self.red_player_video_replay_available = True

    def update_display(self, match):
        # Update display-related variables based on the match data
        self.remaining_time = match.get_remaining_time()
        self.blue_player_score = match.get_player_score('blue')
        self.red_player_score = match.get_player_score('red')
        self.blue_player_penalties = match.get_player_penalties('blue')
        self.red_player_penalties = match.get_player_penalties('red')
        self.blue_player_video_replay_available = match.blue_player.video_replay_available
        self.red_player_video_replay_available = match.red_player.video_replay_available

    def show(self):
        # Implement the display logic to show the information on the external monitor
        # This could be as simple as printing the information or using external display libraries
        print(f"Remaining Time: {self.remaining_time}")
        print(f"Blue Player Score: {self.blue_player_score}  Penalties: {self.blue_player_penalties}")
        print(f"Red Player Score: {self.red_player_score}  Penalties: {self.red_player_penalties}")
        print(f"Blue Player Video Replay Available: {self.blue_player_video_replay_available}")
        print(f"Red Player Video Replay Available: {self.red_player_video_replay_available}")
