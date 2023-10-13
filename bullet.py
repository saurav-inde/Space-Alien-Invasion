
import pygame
from pygame.sprite import Sprite

class CustomBullet(Sprite):
    """A class to manage bullets fired from the player's ship."""

    def __init__(self, space_invaders):
        """Create a bullet object at the player ship's current position."""
        super().__init__()
        self.screen = space_invaders.screen
        self.custom_settings = space_invaders.custom_settings
        self.bullet_color = self.custom_settings.bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.custom_settings.bullet_width,
                                self.custom_settings.bullet_height)
        self.rect.midtop = space_invaders.player_ship.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.custom_settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)
