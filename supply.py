import pygame

pygame.init()

class Supply(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list_Supplies = []
        self.supIndex = 0
        for i in range(2):
            img = pygame.image.load(f'resources/chest/00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
            self.animation_list_Supplies.append(img)
        self.image = self.animation_list_Supplies[self.supIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y + int(self.image.get_height() / 2.4))
        self.counter = 0
        self.animation_speed = 60

    def update(self, scroll):
        self.counter += 1
        if self.counter > self.animation_speed:
            self.counter = 0
            self.supIndex += 1
        if self.supIndex == 2:
            self.supIndex = 0
        self.image = self.animation_list_Supplies[self.supIndex]
        self.rect.x += scroll
