import random
import pygame

BACKGROUND_WIDTH = 480
BACKGROUND_HEIGHT = 700


class GameSpirit(pygame.sprite.Sprite):
    """
    The base class for visible game objects.
    Derived classes will want to override the Sprite.update()
    and assign a Sprite.image and Sprite.rect attributes.
    The initializer can accept any number of Group instances to be added to.
    """
    def __init__(self, img_path, speed=1):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.speed = speed
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += self.speed


class BackgroundSprite(GameSpirit):
    def __init__(self, is_up=False):
        super().__init__("./images/background.png")
        if is_up:
            self.rect.y = -BACKGROUND_HEIGHT

    def update(self):
        super().update()
        if self.rect.y >= BACKGROUND_HEIGHT:
            self.rect.y = -BACKGROUND_HEIGHT


class EnemySpirit(GameSpirit):
    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.rect.x = random.randint(0, BACKGROUND_WIDTH - self.rect.width)
        self.speed = random.randint(0, 5)
        self.rect.bottom = 0

    def update(self):
        super().update()
        if self.rect.y >= BACKGROUND_HEIGHT:
            self.kill()


class HeroSpirit(GameSpirit):
    def __init__(self):
        super().__init__("./images/me1.png")
        self.rect = pygame.Rect(200, 500, 102, 126)
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= BACKGROUND_WIDTH:
            self.rect.right = BACKGROUND_WIDTH

    def fire(self):
        bullet = BulletSpirit()
        bullet.rect.bottom = self.rect.top
        bullet.rect.centerx = self.rect.centerx
        self.bullet_group.add(bullet)


class BulletSpirit(GameSpirit):
    def __init__(self):
        super().__init__("./images/bullet1.png", -10)

    def update(self):
        super().update()
        if self.rect.bottom <= 0:
            self.kill()

