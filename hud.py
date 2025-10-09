import pygame
import settings


class HUD:
    def __init__(self, assets):
        self.assets = assets
        self.font_small = pygame.font.SysFont('helvetica', 20)
        self.font_super_small = pygame.font.SysFont('helvetica', 15)
        self.bar_empty_image = assets.hud_bar_empty
        self.energy_image = assets.hud_energy_bar
        self.additional_bullets_image = pygame.transform.scale_by(assets.hud_bullets_powerup, 0.5)
        self.additional_energy_image = pygame.transform.scale_by(assets.hud_energy_powerup, 0.5)
        self.weapon_images = assets.bullets

    def draw(self, screen, player, game_level, game_points, bullet_type):
        # Health Bar
        ratio = player.hp / settings.PLAYER_HP
        energy_image_ratio = self.energy_image.get_width() * ratio
        energy_text = self.font_super_small.render(f'{player.hp}', True, 'White')
        energy_image_scaled = pygame.transform.scale(self.energy_image,
                                                     (max(0, energy_image_ratio), self.energy_image.get_height()))

        # Weapon Info
        weapon_image = self.weapon_images[bullet_type]
        weapon_qty_text = self.font_small.render(f'{settings.BULLET_DATA[bullet_type]["qty"]}', True, 'White')

        # Game Info
        level_text = self.font_small.render(f'Lvl: {game_level}', True, 'White')
        points_text = self.font_small.render(f'{int(game_points)}', True, 'White')

        # Power-up Prompts
        if game_points >= int((5_000 * game_level) / 3):
            buy_bullets_text = self.font_super_small.render(f'(P)', True, 'White')
            screen.blit(buy_bullets_text, (settings.SCREEN_WIDTH - buy_bullets_text.get_width() - 20, 70))
            screen.blit(self.additional_bullets_image, (settings.SCREEN_WIDTH - 60, 68))

        if game_points >= int((10_000 * game_level) / 3) and player.hp != settings.PLAYER_HP:
            buy_energy_text = self.font_super_small.render(f'(O)', True, 'White')
            screen.blit(buy_energy_text, (settings.SCREEN_WIDTH - buy_energy_text.get_width() - 20, 90))
            screen.blit(self.additional_energy_image, (settings.SCREEN_WIDTH - 60, 88))

        # Blitting everything to the screen
        screen.blit(points_text, (settings.SCREEN_WIDTH - points_text.get_width() - 20, 50))
        screen.blit(level_text, (settings.SCREEN_WIDTH - level_text.get_width() - 20, 17))
        screen.blit(weapon_qty_text, (50, 57))
        screen.blit(self.bar_empty_image, (5, 10))
        screen.blit(energy_image_scaled, (14, 17))
        screen.blit(weapon_image, (8, 50))
        screen.blit(energy_text, (68, 19))