import pygame
import settings


class Assets:
    def __init__(self):
        # Background
        self.background = pygame.image.load('./Graphics/background/bg12.jpeg').convert()

        # Player
        self.player_ship = pygame.image.load('./Graphics/player/ship2.png').convert_alpha()

        # Aliens
        self.aliens = {
            alien_type: pygame.image.load(
                f'./Graphics/aliens/{data["image"]}.png').convert_alpha()
            for alien_type, data in settings.ALIEN_DATA.items()
        }

        # Bullets
        self.bullets = {
            bullet_type: pygame.image.load(
                f'./Graphics/weapons/{data["image"]}.png').convert_alpha()
            for bullet_type, data in settings.BULLET_DATA.items()
        }

        # Power-ups
        self.powerups = {
            powerup_type: pygame.image.load(
                f'./Graphics/powerups/{data["image"]}.png').convert_alpha()
            for powerup_type, data in settings.POWERUP_DATA.items()
        }

        # HUD
        self.hud_bar_empty = pygame.image.load('./Graphics/other/hp_bar_bg.png').convert_alpha()
        self.hud_energy_bar = pygame.image.load('./Graphics/other/hp_bar.png').convert_alpha()
        self.hud_bullets_powerup = pygame.image.load('./Graphics/powerups/bullets.png').convert_alpha()
        self.hud_energy_powerup = pygame.image.load('./Graphics/powerups/energy.png').convert_alpha()

        # Sounds
        self.sound_enabled = True
        try:
            pygame.mixer.init()
            self.player_shot_sound = pygame.mixer.Sound('./Music/sfx_laser1.ogg')
            self.alien_shot_sound = pygame.mixer.Sound('./Music/mixkit-short-laser-gun-shot-1670.wav')
            self.explosion_sound = pygame.mixer.Sound('./Music/mixkit-falling-hit-757.wav')
            self.powerup_sound = pygame.mixer.Sound('./Music/mixkit-space-coin-win-notification-271.wav')
            self.game_over_sound = pygame.mixer.Sound('./Music/sfx_lose.ogg')
            self.player_hit_sound = pygame.mixer.Sound('./Music/sfx_shieldDown.ogg')
            pygame.mixer.music.load('./Music/mixkit-space-deploy-whizz-3003.wav')
        except pygame.error:
            self.sound_enabled = False
            print("Warning: Audio device not found. Running without sound.")