import pygame

class HitText(pygame.sprite.Sprite):
    # noinspection PyTypeChecker
    def __init__(self, entity, damage, color, direction, groups):
        super().__init__(groups)
        self.FONT_kill = pygame.font.SysFont('helvetica', 15)
        self.image = self.FONT_kill.render(damage, True, color)
        self.rect = self.image.get_rect(center=(entity.x, entity.y))
        self.pos = pygame.math.Vector2(self.rect.midtop)
        self.direction = pygame.math.Vector2(0, direction)
        self.velocity = 80
        self.counter = 0

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.counter += 400 * dt
        if self.counter > 200:
            self.kill()