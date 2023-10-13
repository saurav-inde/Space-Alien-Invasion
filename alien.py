
import pygame
from pygame.sprite import Sprite

class CustomAlien(Sprite):
    """A class to represent a single alien in the enemy fleet."""

    def __init__(self, space_invaders):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = space_invaders.screen
        self.custom_settings = space_invaders.custom_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien right or left."""
        self.x += self.custom_settings.alien_speed * self.custom_settings.fleet_direction
        self.rect.x = self.x
