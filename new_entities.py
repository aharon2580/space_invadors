import new_settings as nst
import pygame
st = nst.Settings()


class Player:
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = position[0]
        self.rect.bottom = position[1]

    def move(self, direction, speed, screen):
        if direction == 'right':
            self.rect.move_ip(max(1, st.screen_width // 500) * speed, 0)
        elif direction == 'left':
            self.rect.move_ip(min(-1, - st.screen_width // 500) * speed, 0)
        self.rect.clamp_ip(screen)

    def shoot(self, image):
        return Bullet(image, (self.rect.centerx, self.rect.top))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, life, position, value):
        super().__init__()
        self.image = image
        self.life = life
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.value = value

    def update(self, direction):
        self.rect.move_ip(direction)

    def shoot(self, image):
        return Bullet(image, (self.rect.centerx, self.rect.bottom))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, direction, height):
        self.rect.move_ip(direction)
        if self.rect.bottom > height or self.rect.top < 0:
            self.kill()