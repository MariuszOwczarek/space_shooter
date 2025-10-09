import pygame
import settings


class Powerups(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, power_type, groups, assets):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.power_type = power_type
        self.image = assets.powerups[power_type]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = 100

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
