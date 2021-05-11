""" Project: Sugar Fighting Game

* The image and sound elements are in the download folders

** features:
    → animation
    → sound effect
    → level counter
    
*** to be updated: level up!
    → change background/bombs/sugar enemies
    → set different difficulties
test
"""

import random
import pygame

pygame.init()
pygame.mixer.init()

SCREEN_RECT = pygame.Rect(0, 0, 1467, 974)
FRAME_PER_SEC = 60

SUGAR_FALLING_DOWN = pygame.USEREVENT
DEERTARO_FIRE_EVENT = pygame.USEREVENT + 1
pygame.display.set_caption("Sugar Fighting ❤ dev by Ingrid")
# # set game sounds path ↓
get_coin_sound = pygame.mixer.Sound('./sound/get_coin.wav')
player_die_sound = pygame.mixer.Sound('./sound/game_over.wav')
pygame.mixer.music.load('./sound/bgm.wav')
pygame.mixer.music.set_volume(0.2)

# # learn to define several colors ↓
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)

LEVEL = 1
"""try to print something on the screen"""
font_name = pygame.font.match_font('arial')  # match a similar font in other computers
# ↑ Once I added a font like this, the program is initializing very slow :(
# that's why we need to waif for a few seconds. If I remove the score, the loading is fast


def draw_text(surf, text, size, x, y):
    # font = pygame.font.Font(font_name, size)
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    # font = pygame.font.Font('arial', size)
    text_surface = font.render(text, True, PINK)  # anti aliased: smooth edges
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class SugarFightingGame(object):
    """the main game"""

    def __init__(self):
        print("Initialize the game...")

        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        # todo new added
        SugarFightingGame.__create_user_events()
        self.coin = 0
        self.level = 1

    def __create_sprites(self):
        self.back_group = pygame.sprite.Group(Background(), Background(True))

        # self.deertaro = DeerTaro()
        self.deertaro = DeerTaro()
        self.deertaro_group = pygame.sprite.Group(self.deertaro)

        self.sugar_group = pygame.sprite.Group()
        self.destroy_group = pygame.sprite.Group()

    @staticmethod
    def __create_user_events():
        """set complexity of different levels"""
        # # Frequency of sugar enemies
        pygame.time.set_timer(SUGAR_FALLING_DOWN, 1500)

        # # Frequency of firing the green bombs
        pygame.time.set_timer(DEERTARO_FIRE_EVENT, 800)

    def start_game(self):
        print("Game is starting...")
        pygame.mixer.music.play(loops=-1)  # keep playing the music again: -1
        while True:
            # the game loop is quite template, I take reference from tutorials
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SugarFightingGame.__game_over()
            elif event.type == SUGAR_FALLING_DOWN:
                # sugar_1 = Sugar()
                # self.sugar_group.add(sugar_1)
                self.sugar_group.add(Sugar())

            # press e to end the game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.deertaro.destroyed()

                # explode everything
                for sugar in self.sugar_group.sprites():
                    sugar.destroyed()

            elif event.type == DEERTARO_FIRE_EVENT:
                self.deertaro.fire()

        # todo missing part
        if self.deertaro.can_destroyed:
            SugarFightingGame.__game_over()

        keys_pressed = pygame.key.get_pressed()

        direction = keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT]

        # set deertaro's moving speed
        self.deertaro.speed = direction * 4

    def __check_collide(self):
        # # solution 1: just use a still pic
        # pygame.sprite.groupcollide(self.deertaro.bombs, self.sugar_group, True, True)
        #
        # sugar_enemies = pygame.sprite.spritecollide(self.deertaro, self.sugar_group, True)
        # if len(sugar_enemies) > 0:
        #     self.deertaro.kill()
        #     SugarFightingGame.__game_over()
        # global COIN_COLLECTION

        sugar_enemies = pygame.sprite.groupcollide(self.sugar_group,
                                                   self.deertaro.bombs,
                                                   False,
                                                   True).keys()
        # # solution 2: after level-up, I want to give sugar more lives
        # # so write this part for the future extension
        for sugar in sugar_enemies:
            sugar.life -= 1
            get_coin_sound.play()
            # COIN_COLLECTION += 10
            self.coin += 10
            # print("Coins: {}".format(COIN_COLLECTION))
            print("Coins: {}".format(self.coin))

            if sugar.life <= 0:
                sugar.add(self.destroy_group)
                sugar.remove(self.sugar_group)
                sugar.destroyed()

        # ↓ in the future version, I want to give the player more lives
        # although this is not useful in the version, I still set so
        for deertaro in pygame.sprite.spritecollide(self.deertaro,
                                                    self.sugar_group,
                                                    True):
            self.deertaro.destroyed()
            player_die_sound.play()
            print("Deertaro is dead_(:з」∠)_...")

    def __update_sprites(self):
        for group in [self.back_group, self.deertaro_group,
                      self.deertaro.bombs, self.sugar_group,
                      self.destroy_group]:
            group.update()
            group.draw(self.screen)

        draw_text(self.screen, ("score: " + str(self.coin)), 40, 120, 20)

        # # solution 1: calling method: workable!
        # if 0 <= self.coin < 100:
        #     self.level = 1
        # if 100 <= self.coin < 200:
        #     self.level = 2
        # if 200 <= self.coin < 300:
        #     self.level = 3
        # if 300 <= self.coin < 400:
        #     self.level = 4
        # if self.coin >= 400:
        #     self.level = 666  # to be developed
        #
        # if self.level == 1:
        #     draw_text(self.screen, str("Level 1"), 40, 1300, 20)
        # if self.level == 2:
        #     draw_text(self.screen, str("Level 2"), 40, 1300, 20)
        # if self.level == 3:
        #     draw_text(self.screen, str("Level 3"), 40, 1300, 20)
        # if self.level == 4:
        #     draw_text(self.screen, str("Level 3"), 40, 1300, 20)
        # if self.level == 666:
        #     draw_text(self.screen, str("all beta games deserve to wait..."), 40, 1140, 20)
        #     draw_text(self.screen, str("Congratulations! Press E to exit"), 40, 730, 200)

        # # solution 2: set a global variable: easy to change the level set
        global LEVEL
        if 0 <= self.coin < 100:
            LEVEL = 1
        if 100 <= self.coin < 200:
            LEVEL = 2
        if 200 <= self.coin < 300:
            LEVEL = 3
        if 300 <= self.coin < 400:
            LEVEL = 4
        if self.coin >= 400:
            LEVEL = 666  # to be developed

        if LEVEL == 1:
            draw_text(self.screen, str("Level 1"), 40, 1300, 20)
        if LEVEL == 2:
            draw_text(self.screen, str("Level 2"), 40, 1300, 20)
        if LEVEL == 3:
            draw_text(self.screen, str("Level 3"), 40, 1300, 20)
        if LEVEL == 4:
            draw_text(self.screen, str("Level 3"), 40, 1300, 20)
        if LEVEL == 666:
            draw_text(self.screen, str("all beta games deserve to wait..."), 40, 1140, 20)
            draw_text(self.screen, str("Congratulations! Press E to exit"), 40, 730, 200)

        pygame.display.flip()

    @staticmethod
    def __game_over():
        pygame.quit()
        print("Thank you for your playing!")
        exit()


class GameSprite(pygame.sprite.Sprite):  # sprite modules contain two class: Group & Sprite
    """The game sprite"""

    def __init__(self, image_name, speed=2):
        # calling parent's initial method
        super().__init__()

        # define game sprite's attributes (image, position, speed)
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()  # x, y = 0, 0
        self.speed = speed

    # def update(self):
    #     self.rect.y += self.speed
    def update(self, *args):
        self.rect.top += self.speed

    @staticmethod
    def image_names(prefix, count):
        # names = f"./image/{image_names}i.png"         # make my image name pipelined
        names = []
        for i in range(1, count + 1):
            names.append("./image/" + prefix + str(i) + ".png")
        # print(names)        # for test
        return names


class FightingSprite(GameSprite):
    """DeerTaro & Sugars"""

    def __init__(self, image_names, destroy_names=None, life=None, speed=None):
        image_name = image_names[0]
        super().__init__(image_name, speed)

        self.life = life

        self.__life_images = []
        for file_name in image_names:
            # print("life", file_name)
            image = pygame.image.load(file_name)
            self.__life_images.append(image)

        # destroyed
        self.__destroy_images = []
        for file_name in destroy_names:
            # print("destroy", file_name)
            image = pygame.image.load(file_name)
            self.__destroy_images.append(image)

        # default image of being alive
        self.images = self.__life_images
        # image index
        self.show_image_index = 0
        # if loop the display
        self.is_loop_show = True
        # if can be deleted
        self.can_destroyed = False

    def update(self, *args):
        self.update_images()

        super().update(args)

    def update_images(self):
        """achieve animation by update sprite images"""

        pre_index = int(self.show_image_index)
        self.show_image_index += 0.2
        count = len(self.images)

        # if loop:
        if self.is_loop_show:
            self.show_image_index %= len(self.images)
        elif self.show_image_index > count - 1:
            self.show_image_index = count - 1
            self.can_destroyed = True

        current_index = int(self.show_image_index)

        if pre_index != current_index:
            self.image = self.images[current_index]

    def destroyed(self):
        """get collided"""
        # default image of being destroyed
        self.images = self.__destroy_images
        # image index
        self.show_image_index = 0
        # if loop the display
        self.is_loop_show = False


class Background(GameSprite):
    """Game's background sprite"""
    # workable version↓
    def __init__(self, is_alternative_pic=False):
        super().__init__("./image/bg1.png")
        if is_alternative_pic:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Sugar(FightingSprite):
    """Sugar friends: coke, lollipop, macaron, donut, bubble tea, etc."""

    def __init__(self):
        image_names = ["./image/sugar1.png"]
        destroy_names = GameSprite.image_names("coin", 7)
        super().__init__(image_names, destroy_names, 1, 2)

        self.speed = random.randint(1, 4)

        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self, *args):
        super().update(args)
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

        # todo new added
        if self.can_destroyed:
            self.kill()

    def __del__(self):
        # print("Sugar is killed!")         # for test
        pass


class OrganicBomb(GameSprite):
    """deertaro's bullet to fight with the sugar"""
    """in this version I use cabbage!!"""

    def __init__(self):
        super().__init__("./image/green1.png", -3)  # cabbage: 36*33;

    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("The bomb was successfully recalled")  # for test
        pass


class DeerTaro(FightingSprite):
    """the main character 'DeerTaro' sprite"""

    # def __init__(self):
    def __init__(self):
        # super().__init__("./image/deertaro.png", 0)       # deertaro: 114*152
        # ↓
        # deertaro_image = "./image/deertaro1.png"
        # super().__init__(deertaro_image, 1)

        # image_names = GameSprite.image_names("./image/deertaro", 2)
        image_names = GameSprite.image_names("deertaro", 4)
        # destroy_names = GameSprite.image_names("./image/pink_explode", 10)
        destroy_names = GameSprite.image_names("pink_explode", 11)

        super().__init__(image_names, destroy_names, 0, 3)
        # print("Now DeerTaro's lives are:", self.life)

        # player's initial position
        self.rect.centerx = SCREEN_RECT.centerx  # centerx = x + width/2
        self.rect.bottom = SCREEN_RECT.bottom - 10

        # creat a bomb sprite group
        self.bombs = pygame.sprite.Group()

    def update(self):
        """rewrite the update method for DeerTaro"""
        # todo new added:
        self.update_images()

        # Move horizontally
        self.rect.x += self.speed

        # detect if my character get out of the screen!
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:  # right = x + width
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("Fire!")  # for test
        cabbage = OrganicBomb()

        cabbage.rect.bottom = self.rect.y - 20
        cabbage.rect.centerx = self.rect.centerx

        self.bombs.add(cabbage)


if __name__ == '__main__':
    game = SugarFightingGame()

    game.start_game()
