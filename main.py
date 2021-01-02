import os
import sys
import random
import pygame


def game():
    running = True
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    player_sprites = pygame.sprite.Group()

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

    class Player(pygame.sprite.Sprite):
        image = load_image('player.png')
        image = pygame.transform.scale(image, (235, 165))

        def __init__(self, x, y):
            super().__init__(player_sprites)
            self.image = Player.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (x, y)
            self.rect.size = (self.rect.w // 10, self.rect.h // 10)

    clock = pygame.time.Clock()
    fps = 60
    Player(width // 2, height // 2)
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
        player_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == CHANGEBGEVENT:
                timer_start = False
                next_color = random_color()
                r_add = (next_color[0] - color[0]) / 2000
                g_add = (next_color[1] - color[1]) / 2000
                b_add = (next_color[2] - color[2]) / 2000
                print(r_add, b_add, g_add)
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

                print(color, next_color, (r_add, g_add, b_add) == (0, 0, 0), (r_add, g_add, b_add))
                if (r_add, g_add, b_add) == (0, 0, 0) and not timer_start:
                    timer_start = True
                    pygame.time.set_timer(CHANGEBGEVENT, 5000)
                else:
                    pygame.time.set_timer(CHANGEBGEVENT_SECOND, 1)


        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    game()
