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
    atack_sprites = pygame.sprite.Group()
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

    class Attack(pygame.sprite.Sprite):
        original_image = load_image('attack.png')
        original_image = pygame.transform.smoothscale(original_image, (10, 10))
        speed = 10

        def __init__(self, x, y):
            super().__init__(atack_sprites)
            self.angle = math.radians(-player.angle)
            self.image = Attack.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))

        def update(self):
            self.rect.center = calculate_new_xy(self.rect.center, self.speed, self.angle)

    class Player(pygame.sprite.Sprite):
        original_image = load_image('player.png')
        original_image = pygame.transform.smoothscale(original_image, (118, 83))
        angle = 0

        def __init__(self, x, y):
            super().__init__(player_sprites)
            self.pos = (x, y)
            self.image = Player.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))
            # self.mask = pygame.mask.from_surface(self.image)
            # self.rect.center = (x, y)
            self.rect.size = (self.rect.w, self.rect.h)

        def rotate(self, mouse_x, mouse_y):
            rel_x, rel_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
            # angle = math.atan2(rel_y, rel_x)
            self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.original_image, int(self.angle))
            self.rect = self.image.get_rect(center=self.pos)

        def update(self):
            pass

    clock = pygame.time.Clock()
    mouse_last_pos = (0, 0)
    player = Player(width // 2, height // 2)

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
        atack_sprites.draw(screen)
        player_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Attack(width // 2, height // 2)
            if event.type == pygame.MOUSEMOTION:
                if 150 >= math.hypot(pygame.mouse.get_pos()[0] - width // 2,
                                     pygame.mouse.get_pos()[1] - height // 2) <= 250:
                    mouse_last_pos = pygame.mouse.get_pos()
                player.rotate(mouse_x=pygame.mouse.get_pos()[0], mouse_y=pygame.mouse.get_pos()[1])

            if event.type == CHANGEBGEVENT:
                timer_start = False
                next_color = random_color()
                r_add = (next_color[0] - color[0]) / 2000
                g_add = (next_color[1] - color[1]) / 2000
                b_add = (next_color[2] - color[2]) / 2000
                pygame.time.set_timer(CHANGEBGEVENT_SECOND, 16)
            if event.type == CHANGEBGEVENT_SECOND and next_color != color:
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
        atack_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    game()
