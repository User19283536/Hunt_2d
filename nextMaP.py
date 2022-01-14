import pygame

pygame.init()

class NextMap(pygame.sprite.Sprite):
    def __init__(self, img, x, y, block_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + block_size // 2, y + (block_size - self.image.get_height()))
        self.completed = False

    def update(self, screen_shift, player):
        self.rect.x += screen_shift
        if pygame.sprite.collide_rect(self, player):
            self.completed = True





