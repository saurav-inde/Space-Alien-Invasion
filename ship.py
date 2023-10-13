
import pygame


class CustomShip:
    """A class to manage the player's ship."""

    def __init__(self, space_invaders):
        """Initialize the player's ship and set its starting position."""
        self.screen = space_invaders.screen
        self.custom_settings = space_invaders.custom_settings
        self.screen_rect = space_invaders.screen.get_rect()

        # Load the player's ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flags; start with a ship that's not moving.
        self.move_right = False
        self.move_left = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.custom_settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.x -= self.custom_settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
