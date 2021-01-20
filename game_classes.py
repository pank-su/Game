import math
import os
import random
import sys

import pygame

width, height = 500, 500
size = width, height
screen = pygame.display.set_mode(size)


def change_dif(chance: float) -> bool:
    one_part = chance * 100
    ran_number = random.randint(1, 100)
    return ran_number < one_part


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

    def __init__(self, x, y, group):
        super().__init__(group)
        self.pos = (x, y)
        self.image = Player_live.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))


class Enemy(pygame.sprite.Sprite):
    original_image = load_image('bad_guy.png')
    original_image = pygame.transform.smoothscale(original_image, (45, 50))

    def __init__(self, x, y, group, speed=3, lives=1):
        super().__init__(group)
        self.pos = (x, y)
        self.speed = speed
        self.lives = lives
        self.image = Enemy.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        step_to_x = width // 2 - x
        step_to_y = height // 2 - y
        self.angle = ((180 / math.pi) * -math.atan2(step_to_y, step_to_x))

    def update(self, tank, player):
        if (self.rect.centerx > 425 or self.rect.centerx < 75) or (
                self.rect.centery > 425 or self.rect.centery < 75):
            step_to_x = width // 2 - self.rect.centerx
            step_to_y = height // 2 - self.rect.centery
            self.angle = ((180 / math.pi) * -math.atan2(step_to_y, step_to_x))
        if width // 2 == self.rect.centerx and height // 2 == self.rect.centery:
            print('bug')
        if self.lives == 0:
            player.score += 1
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

    def __init__(self, x, y, group, player):
        super().__init__(group)
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

    score = 0

    def __init__(self, x, y, group):
        super().__init__(group)
        self.lives_obj = [Player_live(width - 44 + 20, 20, group),
                          Player_live(width - 44 * 2 + 20, 20, group),
                          Player_live(width - 44 * 3 + 20, 20, group)]
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
            self.lives_obj[len(self.lives_obj) - (len(self.lives_obj) - self.lives)].kill()


class Tank(pygame.sprite.Sprite):
    original_image = load_image('tank_1.png')
    original_image = pygame.transform.smoothscale(original_image, (80, 80))

    def __init__(self, x, y, group):
        super().__init__(group)
        self.pos = (x, y)
        self.image = Tank.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect.center = (x, y)
        self.rect.size = (self.rect.w, self.rect.h)


class Game():
    screen = screen
    spawn_in_iter = 1
    time_to_iter = 2000
    enemy_lives = 1
    fps = 60
    difficult = 1
    enemy_speed = 3
    chance = 0.1
    last_change_score = 0
    last_score = 0
    running = True

    def __init__(self):
        pygame.init()
        self.player_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.tank = Tank(width // 2, height // 2, self.player_sprites)
        self.player = Player(width // 2, height // 2, self.player_sprites)
        Enemy(-50, -50, self.enemy_sprites)
        self.SPAWNENEMYEVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SPAWNENEMYEVENT, 2000)
        self.color = random_color()
        self.CHANGEBGEVENT = pygame.USEREVENT + 1
        self.CHANGEBGEVENT_SECOND = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CHANGEBGEVENT, 1000)
        self.font = pygame.font.Font('images/font.ttf', 48)

    def start(self):
        next_color = random_color()
        r_add = (next_color[0] - self.color[0]) / 2000
        g_add = (next_color[1] - self.color[1]) / 2000
        b_add = (next_color[2] - self.color[2]) / 2000
        while self.running:
            if self.player.score - self.last_change_score > 0 and self.last_score != self.player.score:
                if change_dif(self.chance):
                    self.difficult += 1
                    last_change_score = self.player.score
                    self.chance = (0.2 / self.difficult) * (self.player.score - last_change_score)
                else:
                    self.chance = (0.2 / self.difficult) * (
                            self.player.score - self.last_change_score)
                self.last_score = self.player.score
            if self.difficult == 2:
                self.enemy_speed = 4
            if self.difficult == 3:
                self.time_to_iter = 1500
                self.enemy_lives = random.randint(1, 2)
            if self.difficult == 4:
                self.time_to_iter = 1400
                self.enemy_speed = 5
                self.enemy_lives = random.randint(1, 2)
            if self.difficult == 5:
                self.spawn_in_iter = 2
                self.enemy_lives = random.randint(1, 2)
            if self.difficult == 6:
                self.time_to_iter = 1000
                self.enemy_lives = random.randint(1, 2)

            # print(self.difficult, self.chance)
            try:
                normal_color = tuple(map(int, self.color))
                self.screen.fill(normal_color)
            except:
                pass
            self.attack_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            text = self.font.render(str(self.player.score), True, (255, 255, 255))
            self.screen.blit(text, (width // 2 - 17, 0))
            if self.player.lives == 0:
                self.running = False
            list = pygame.sprite.groupcollide(self.attack_sprites, self.enemy_sprites, True, False)
            if list:
                for key in list.keys():
                    for enemy in list[key]:
                        enemy.lives -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Attack(width // 2, height // 2, self.attack_sprites, self.player)
                elif event.type == pygame.MOUSEMOTION:
                    # if 150 >= math.hypot(pygame.mouse.get_pos()[0] - width // 2,
                    #                      pygame.mouse.get_pos()[1] - height // 2) <= 250:
                    #     mouse_last_pos = pygame.mouse.get_pos()
                    self.player.rotate(mouse_x=pygame.mouse.get_pos()[0],
                                       mouse_y=pygame.mouse.get_pos()[1])
                elif event.type == self.SPAWNENEMYEVENT:
                    for i in range(self.spawn_in_iter):
                        xy = (1, 1)
                        while (xy[0] > 0 and xy[1] > 0) and (xy[0] < width and xy[1] < height):
                            xy = (random.randint(-100, width + 100),
                                  random.randint(-100, height + 100))
                        print(xy)
                        Enemy(xy[0], xy[1], self.enemy_sprites, speed=self.enemy_speed,
                              lives=self.enemy_lives)
                    pygame.time.set_timer(self.SPAWNENEMYEVENT, self.time_to_iter)
                elif event.type == self.CHANGEBGEVENT:
                    timer_start = False
                    next_color = random_color()
                    r_add = (next_color[0] - self.color[0]) / 2000
                    g_add = (next_color[1] - self.color[1]) / 2000
                    b_add = (next_color[2] - self.color[2]) / 2000
                    pygame.time.set_timer(self.CHANGEBGEVENT_SECOND, 16)
                elif event.type == self.CHANGEBGEVENT_SECOND and next_color != self.color:
                    if r_add < 0 and next_color[0] > self.color[0]:
                        r_add = 0
                    if g_add < 0 and next_color[1] > self.color[1]:
                        g_add = 0
                    if b_add < 0 and next_color[2] > self.color[2]:
                        b_add = 0
                    if r_add > 0 and next_color[0] < self.color[0]:
                        r_add = 0
                    if g_add > 0 and next_color[1] < self.color[1]:
                        g_add = 0
                    if b_add > 0 and next_color[2] < self.color[2]:
                        b_add = 0

                    self.color = (
                        self.color[0] + r_add, self.color[1] + g_add, self.color[2] + b_add)
                    if (r_add, g_add, b_add) == (0, 0, 0) and not timer_start:
                        timer_start = True
                        pygame.time.set_timer(self.CHANGEBGEVENT, 5000)
                    else:
                        pygame.time.set_timer(self.CHANGEBGEVENT_SECOND, 1)
            self.player_sprites.update()
            self.attack_sprites.update()
            self.enemy_sprites.update(self.tank, self.player)
            pygame.display.flip()
            self.clock.tick(self.fps)
        return self.player.score


if __name__ == '__main__':
    game_ = Game()
    scores = game_.start()
    with open('scores.txt', 'w') as file:
        file.write(str(scores))
    pygame.display.quit()
