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
        rgbl = [255, 0, 0]
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

    Player(width // 2, height // 2)
    while running:
        screen.fill(random_color())
        player_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()


if __name__ == '__main__':
    game()
