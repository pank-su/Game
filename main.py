import math
import os
import random
import sys

import pygame


def game():
    running = True
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    player_sprites = pygame.sprite.Group()
    attack_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    fps = 60

    def random_color():
        rgbl = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        random.shuffle(rgbl)
        return tuple(rgbl)

    def load_image(name, colorkey=None):
        fullname = os.path.join('images', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def calculate_new_xy(old_xy, speed, angle_in_radians):
        new_x = old_xy[0] + (speed * math.cos(angle_in_radians))
        new_y = old_xy[1] + (speed * math.sin(angle_in_radians))
        return new_x, new_y

    class Player_live(pygame.sprite.Sprite):
        original_image = load_image('live.png')
        original_image = pygame.transform.smoothscale(original_image, (44, 36))

        def __init__(self, x, y):
            super().__init__(player_sprites)
            self.pos = (x, y)
            self.image = Player_live.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))

    class Enemy(pygame.sprite.Sprite):
        original_image = load_image('bad_guy.png')
        original_image = pygame.transform.smoothscale(original_image, (45, 50))

        def __init__(self, x, y, speed=3, lives=1):
            super().__init__(enemy_sprites)
            self.pos = (x, y)
            self.speed = speed
            self.lives = lives
            self.image = Enemy.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
            step_to_x = width // 2 - x
            step_to_y = height // 2 - y
            self.angle = ((180 / math.pi) * -math.atan2(step_to_y, step_to_x))

        def update(self):
            if (self.rect.centerx > 500 or self.rect.centerx < 0) or (self.rect.centery > 500 or self.rect.centery < 0):
                step_to_x = width // 2 - self.rect.centerx
                step_to_y = height // 2 - self.rect.centery
                self.angle = ((180 / math.pi) * -math.atan2(step_to_y, step_to_x))
            if self.lives == 0:
                self.kill()
            self.image = pygame.transform.rotate(self.original_image, int(self.angle))
            if not pygame.sprite.collide_mask(self, player) and not pygame.sprite.collide_mask(self,
                                                                                               tank):
                self.rect.center = calculate_new_xy(self.rect.center, self.speed,
                                                    math.radians(-self.angle))
            else:
                player.lives -= 1
                self.kill()

    class Attack(pygame.sprite.Sprite):
        original_image = load_image('attack.png')
        original_image = pygame.transform.smoothscale(original_image, (10, 10))
        speed = 10

        def __init__(self, x, y):
            super().__init__(attack_sprites)
            self.angle = math.radians(-player.angle)
            self.image = Attack.original_image.copy()

            new_x, new_y = x, y
            new_x += (player.rect.w // 2 - 20) * (
                1 if pygame.mouse.get_pos()[0] > width // 2 else -1)
            new_y += (player.rect.h // 2 - 20) * (
                1 if pygame.mouse.get_pos()[1] > height // 2 else -1)
            self.rect = self.image.get_rect(center=(new_x, new_y))

        def update(self):
            self.rect.center = calculate_new_xy(self.rect.center, self.speed, self.angle)

    class Player(pygame.sprite.Sprite):
        original_image = load_image('tank_5.png')
        # original_image = pygame.transform.smoothscale(original_image, (118, 90))
        original_image = pygame.transform.smoothscale(original_image, (150, 48))
        angle = 0
        lives = 3
        lives_obj = [Player_live(width - 44 + 20, 20), Player_live(width - 44 * 2 + 20, 20),
                     Player_live(width - 44 * 3 + 20, 20)]

        def __init__(self, x, y):
            super().__init__(player_sprites)
            self.pos = (x, y)
            self.image = Player.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
            # self.rect.center = (x, y)
            self.rect.size = (self.rect.w, self.rect.h)

        def rotate(self, mouse_x, mouse_y):
            rel_x, rel_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
            # angle = math.atan2(rel_y, rel_x)
            self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.original_image, int(self.angle))
            self.rect = self.image.get_rect(center=self.pos)

        def update(self):
            if self.lives < len(self.lives_obj):
                self.lives_obj[len(self.lives_obj) -1].kill()


    class Tank(pygame.sprite.Sprite):
        original_image = load_image('tank_1.png')
        original_image = pygame.transform.smoothscale(original_image, (80, 80))

        def __init__(self, x, y):
            super().__init__(player_sprites)
            self.pos = (x, y)
            self.image = Tank.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))
            self.mask = pygame.mask.from_surface(self.image)
            # self.rect.center = (x, y)
            self.rect.size = (self.rect.w, self.rect.h)

    clock = pygame.time.Clock()
    tank = Tank(width // 2, height // 2)
    player = Player(width // 2, height // 2)

    Enemy(-50, -50)
    SPAWNENEMYEVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWNENEMYEVENT, 2000)
    color = random_color()
    CHANGEBGEVENT = pygame.USEREVENT + 1
    CHANGEBGEVENT_SECOND = pygame.USEREVENT + 2
    pygame.time.set_timer(CHANGEBGEVENT, 1000)
    while running:
        try:
            normal_color = tuple(map(int, color))
            screen.fill(normal_color)
        except:
            pass
        attack_sprites.draw(screen)
        player_sprites.draw(screen)
        enemy_sprites.draw(screen)
        if player.lives == 0:
            running = False
        list = pygame.sprite.groupcollide(attack_sprites, enemy_sprites, True, False)
        if list:
            for key in list.keys():
                for enemy in list[key]:
                    enemy.lives -= 1
                    print(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Attack(width // 2, height // 2)
            elif event.type == pygame.MOUSEMOTION:
                if 150 >= math.hypot(pygame.mouse.get_pos()[0] - width // 2,
                                     pygame.mouse.get_pos()[1] - height // 2) <= 250:
                    mouse_last_pos = pygame.mouse.get_pos()
                player.rotate(mouse_x=pygame.mouse.get_pos()[0], mouse_y=pygame.mouse.get_pos()[1])
            elif event.type == SPAWNENEMYEVENT:
                xy = (1, 1)
                while (xy[0] > 0 and xy[1] > 0) or (xy[0] < 500 and xy[1] < 500):
                    xy = (random.randint(-700, 700), random.randint(-700, 700))
                print(xy)
                Enemy(xy[0], xy[1])
            elif event.type == CHANGEBGEVENT:
                timer_start = False
                next_color = random_color()
                r_add = (next_color[0] - color[0]) / 2000
                g_add = (next_color[1] - color[1]) / 2000
                b_add = (next_color[2] - color[2]) / 2000
                pygame.time.set_timer(CHANGEBGEVENT_SECOND, 16)
            elif event.type == CHANGEBGEVENT_SECOND and next_color != color:
                if r_add < 0 and next_color[0] > color[0]:
                    r_add = 0
                if g_add < 0 and next_color[1] > color[1]:
                    g_add = 0
                if b_add < 0 and next_color[2] > color[2]:
                    b_add = 0
                if r_add > 0 and next_color[0] < color[0]:
                    r_add = 0
                if g_add > 0 and next_color[1] < color[1]:
                    g_add = 0
                if b_add > 0 and next_color[2] < color[2]:
                    b_add = 0

                color = (color[0] + r_add, color[1] + g_add, color[2] + b_add)
                if (r_add, g_add, b_add) == (0, 0, 0) and not timer_start:
                    timer_start = True
                    pygame.time.set_timer(CHANGEBGEVENT, 5000)
                else:
                    pygame.time.set_timer(CHANGEBGEVENT_SECOND, 1)
        player_sprites.update()
        attack_sprites.update()
        enemy_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    game()
