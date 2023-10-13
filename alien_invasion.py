
import sys
from time import sleep
import pygame
from pygame import mixer
from settings import CustomGameSettings
from game_stats import CustomGameStatistics
from ship import CustomShip
from bullet import CustomBullet
from alien import CustomAlien

# Initializing the mixer
mixer.init()

# Loading the background music
mixer.music.load("sound.wav")

# Setting the volume for the background music
mixer.music.set_volume(0.7)


class SpaceInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.custom_settings = CustomGameSettings()

        self.screen = pygame.display.set_mode(
            (self.custom_settings.screen_width, self.custom_settings.screen_height))
        pygame.display.set_caption("Space Invasion")

        # Create an instance to store game statistics.
        self.game_statistics = CustomGameStatistics(self)

        self.player_ship = CustomShip(self)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_aliens = pygame.sprite.Group()

        self._create_enemy_fleet()

        # Start Space Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.player_ship.update()
                self._update_player_bullets()
                self._update_enemy_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.player_ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.player_ship.move_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_player_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.player_ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.player_ship.move_left = False

    def _fire_player_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.player_bullets) < self.custom_settings.player_bullets_allowed:
            new_bullet = CustomBullet(self)
            self.player_bullets.add(new_bullet)
            mixer.music.play()

    def _update_player_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.player_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.player_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.player_bullets.remove(bullet)

        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        """Respond to bullet-enemy collisions."""
        # Remove any bullets and enemies that have collided.
        collisions = pygame.sprite.groupcollide(
            self.player_bullets, self.enemy_aliens, True, True)

        if not self.enemy_aliens:
            # Destroy existing bullets and create a new fleet.
            self.player_bullets.empty()
            self._create_enemy_fleet()

    def _player_ship_hit(self):
        """Respond to the player ship being hit by an enemy."""
        if self.game_statistics.ships_left > 0:
            # Decrement ships_left.
            self.game_statistics.ships_left -= 1

            # Get rid of any remaining bullets and enemies.
            self.player_bullets.empty()
            self.enemy_aliens.empty()

            # Create a new fleet and center the player ship.
            self._create_enemy_fleet()
            self.player_ship.center_player_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False

    def _update_enemy_aliens(self):
        """Update the positions of all enemies in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.enemy_aliens.update()

        # Look for enemy-ship collisions.
        if pygame.sprite.spritecollideany(self.player_ship, self.enemy_aliens):
            self._player_ship_hit()

        # Look for enemies hitting the bottom of the screen.
        self._check_enemies_bottom()

    def _check_enemies_bottom(self):
        """Check if any enemies have reached the bottom of the screen."""
        for enemy in self.enemy_aliens.sprites():
            if enemy.rect.bottom >= self.custom_settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._player_ship_hit()
                break

    def _create_enemy_fleet(self):
        """Create the fleet of enemies."""
        # Create an enemy and keep adding enemies until there's no room left.
        # Spacing between enemies is one enemy width and one enemy height.
        enemy = CustomAlien(self)
        enemy_width, enemy_height = enemy.rect.size

        current_x, current_y = enemy_width, enemy_height
        while current_y < (self.custom_settings.screen_height - 3 * enemy_height):
            while current_x < (self.custom_settings.screen_width - 2 * enemy_width):
                self._create_enemy(current_x, current_y)
                current_x += 2 * enemy_width

            # Finished a row; reset x value, and increment y value.
            current_x = enemy_width
            current_y += 2 * enemy_height

    def _create_enemy(self, x_position, y_position):
        """Create an enemy and place it in the fleet."""
        new_enemy = CustomAlien(self)
        new_enemy.x = x_position
        new_enemy.rect.x = x_position
        new_enemy.rect.y = y_position
        self.enemy_aliens.add(new_enemy)

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemy_aliens.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for enemy in self.enemy_aliens.sprites():
            enemy.rect.y += self.custom_settings.fleet_drop_speed
        self.custom_settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.custom_settings.background_color)
        for bullet in self.player_bullets.sprites():
            bullet.draw_bullet()
        self.player_ship.blitme()
        self.enemy_aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    space_invaders = SpaceInvasion()
    space_invaders.run_game()
