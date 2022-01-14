import pygame

pygame.init()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list_Coin = []
        self.coinIndex = 0
        for i in range(4):
            img = pygame.image.load(f'resources/coin/00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
            self.animation_list_Coin.append(img)
        self.image = self.animation_list_Coin[self.coinIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y + int(self.image.get_height() / 2.4))
        self.counter = 0
        self.animation_speed = 7

    def update(self, scroll):
        self.counter += 1
        if self.counter > self.animation_speed:
            self.counter = 0
            self.coinIndex += 1
        if self.coinIndex == 4:
            self.coinIndex = 0
        self.image = self.animation_list_Coin[self.coinIndex]

        self.rect.x += scroll
