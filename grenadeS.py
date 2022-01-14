import pygame
import explosion

pygame.init()

grenade_img = pygame.image.load('resources/misc/grenade.png')
grenade_img = pygame.transform.scale(grenade_img,(int(grenade_img.get_width() * 0.5), int(grenade_img.get_height() * 0.5)))

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, flip, scroll, gravity):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.ySpeed = 9
        self.speed = 4
        self.gravity = gravity
        self.scrollAdjust = scroll
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = flip

    def update(self, collision, scroll, sound, group):
        self.rect.x += scroll
        self.ySpeed -= self.gravity
        if self.scrollAdjust > 0:
            dx = self.speed + self.scrollAdjust
        else:
            dx = self.speed - self.scrollAdjust

        dy = -self.ySpeed

        for block in collision:
            if block[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.direction = not self.direction
                dy = 0
                dx = 0
                self.ySpeed = 0

            if block[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if self.ySpeed < 0:
                    self.ySpeed = 0
                    self.speed = 0
                    dy = 0
                    dx = 0

                elif self.ySpeed >= 0:
                    self.ySpeed = 0
                    dy = 4
                    dx = 0

        if self.direction is False:
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.rect.x -= dx
            self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosions = explosion.Explosion(self.rect.x, self.rect.y)
            group.add(explosions)
            sound.play()
