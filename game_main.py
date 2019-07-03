import pygame
from game_spirits import *

EVENT_CREATE_ENEMY = pygame.USEREVENT
EVENT_FIRE = pygame.USEREVENT + 1


class PlaneMain:
    def __init__(self):
        self.__init_game()
        self.__create_spirit()
        pygame.time.set_timer(EVENT_CREATE_ENEMY, 1000)
        pygame.time.set_timer(EVENT_FIRE, 200)

    def __init_game(self):
        pygame.init()
        pygame.display.set_caption("飞机大战")
        self.screen = pygame.display.set_mode((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.Group()

    def __create_spirit(self):
        bg = BackgroundSprite()
        bg_up = BackgroundSprite(True)
        self.background_group = pygame.sprite.Group(bg, bg_up)

        self.hero = HeroSpirit()
        self.hero_group = pygame.sprite.Group(self.hero)

        self.enemy_group = pygame.sprite.Group()

        self.group.add(self.background_group, self.hero_group)
        pass

    def start_game(self):
        while True:
            self.clock.tick(60)
            self.__handle_event()
            self.__check_collide()
            self.__update_spirit()

    def __update_spirit(self):
        self.group.add(self.hero.bullet_group, self.enemy_group)
        self.group.update()
        self.group.draw(self.screen)
        pygame.display.update()

    def __handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.hero.speed = 8
        elif keys[pygame.K_LEFT]:
            self.hero.speed = -8
        else:
            self.hero.speed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneMain.__game_over()
            elif event.type == EVENT_CREATE_ENEMY:
                enemy_new = EnemySpirit()
                self.enemy_group.add(enemy_new)
            elif event.type == EVENT_FIRE:
                self.hero.fire()

    @staticmethod
    def __game_over():
        print("退出游戏……")
        pygame.quit()
        exit()

    def __check_collide(self):
        pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, True, True)
        hero_dict = pygame.sprite.groupcollide(self.hero_group, self.enemy_group, True, False)
        if len(hero_dict) > 0:
            PlaneMain.__game_over()


if __name__ == '__main__':
    PlaneMain().start_game()
