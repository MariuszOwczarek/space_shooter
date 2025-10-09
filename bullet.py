import pygame
import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, bullet_type, resize, groups, assets):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.bullet_type = bullet_type
        self.damage = settings.BULLET_DATA[bullet_type]["damage"]
        self.qty = settings.BULLET_DATA[bullet_type]["qty"]
        image_big = assets.bullets[bullet_type]
        self.image = pygame.transform.scale_by(image_big, resize)
        self.rect = self.image.get_rect(midbottom=pos)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, direction)
        self.velocity = settings.BULLET_DATA[bullet_type]["velocity"]

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
