import pygame
import settings


class Alien(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, alien_type, group, assets):
        super().__init__(group)
        self.alien_type = alien_type
        self.damage = settings.ALIEN_DATA[alien_type]["damage"]
        self.hp = settings.ALIEN_DATA[alien_type]["hp"]
        self.defence = settings.ALIEN_DATA[alien_type]["defence"]
        self.max_hp = self.hp
        self.max_defence = self.defence
        image_big = assets.aliens[self.alien_type]
        self.image = pygame.transform.scale_by(image_big, 0.5)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = 100

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
