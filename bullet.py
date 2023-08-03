import pygame
import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, bullet_type, resize, groups):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.bullet_type = bullet_type
        self.damage = settings.BULLET_DATA[bullet_type]["damage"]
        self.qty = settings.BULLET_DATA[bullet_type]["qty"]
        self.image_big = pygame.image.load(
            f'./Graphics/weapons/{settings.BULLET_DATA[bullet_type]["image"]}.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image_big, resize)
        self.rect = self.image.get_rect(midbottom=pos)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, direction)
        self.velocity = settings.BULLET_DATA[bullet_type]["velocity"]

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
