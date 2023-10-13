
class CustomGameStatistics:
    """Track game statistics for Space Invasion."""

    def __init__(self, space_invasion):
        """Initialize game statistics."""
        self.custom_settings = space_invasion.custom_settings
        self.initialize_stats()

    def initialize_stats(self):
        """Initialize game statistics that can change during gameplay."""
        self.remaining_ships = self.custom_settings.ship_limit
