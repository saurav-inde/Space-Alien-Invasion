
class CustomGameSettings:
    """A class to store all settings for Space Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)

        # Player ship settings
        self.ship_speed = 15
        self.ship_limit = 3

        # Player bullet settings
        self.bullet_speed = 8
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.player_bullets_allowed = 3

        # Enemy alien settings
        self.alien_speed = 2
        self.fleet_drop_speed = 15
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
