import pygame

pygame.init()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = pygame.image.load('resources/misc/bullet.png')
        bullet_img = pygame.transform.scale(bullet_img,(int(bullet_img.get_width() * 0.1), int(bullet_img.get_height() * 0.1)))
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = flip

    def update(self, collision, screen_width):
        if self.direction is False:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()

        for block in collision:
            if block[1].colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.kill()