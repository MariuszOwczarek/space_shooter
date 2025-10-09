import sys
import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.hp = settings.PLAYER_HP
        self.modificator = settings.PLAYER_MODIFICATOR
        self.image = pygame.transform.scale_by(assets.player_ship, 0.5)
        self.rect = self.image.get_rect(midbottom=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT))

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = 380

    def movements(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x - self.velocity * dt >= 0:
            self.direction = pygame.math.Vector2(-1, 0)
            self.pos += self.direction * self.velocity * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if keys[
            pygame.K_d] and self.rect.x + self.velocity * dt + \
                self.rect.width <= settings.SCREEN_WIDTH:
            self.direction = pygame.math.Vector2(1, 0)
            self.pos += self.direction * self.velocity * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if keys[
            pygame.K_s] and self.rect.y + self.velocity * dt + \
                self.rect.height <= settings.SCREEN_HEIGHT:
            self.direction = pygame.math.Vector2(0, 1)
            self.pos += self.direction * self.velocity * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if keys[
            pygame.K_w] and self.rect.y - self.velocity * dt >= 0 \
                and self.rect.y >= 400:
            self.direction = pygame.math.Vector2(0, -1)
            self.pos += self.direction * self.velocity * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.movements(dt)
