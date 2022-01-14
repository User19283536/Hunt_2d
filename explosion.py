import pygame

pygame.init()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list_Explosion = []
        self.expIndex = 0
        for i in range(7):
            img = pygame.image.load(f'resources/explosion/0{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
            self.animation_list_Explosion.append(img)
        self.image = self.animation_list_Explosion[self.expIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 0
        self.animation_speed = 4

    def update(self, scroll):
        self.timer += 1

        if self.timer > self.animation_speed:
            self.timer = 0
            self.expIndex += 1
            self.image = self.animation_list_Explosion[self.expIndex]

            if self.expIndex == 6:
                self.kill()
        self.rect.x += scroll