import pygame
import random

pygame.init()
pygame.font.init()

grav_constant = 0.25
screen_width = 1300
screen_height = 640
bullet_img = pygame.image.load('resources/misc/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * 0.1), int(bullet_img.get_height() * 0.1)))
bullet_dmg = 50
explosion_dmg = 20

block_size = 40

grenade_img = pygame.image.load('resources/misc/grenade.png')
grenade_img = pygame.transform.scale(grenade_img,
                                     (int(grenade_img.get_width() * 0.5), int(grenade_img.get_height() * 0.5)))


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


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, flip, scroll):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.ySpeed = 9
        self.speed = 4
        self.scrollAdjust = scroll
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = flip

    def update(self, collision, scroll, sound):
        self.rect.x += scroll
        self.ySpeed -= grav_constant
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
            explosion = Explosion(self.rect.x, self.rect.y)
            explosions_group.add(explosion)
            sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = flip

    def update(self, collision):
        if self.direction is False:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()

        for block in collision:
            if block[1].colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.kill()


bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
supplies_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()


class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, char_type, def_x, def_y, def_scale, def_speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.scale = def_scale
        self.speed = def_speed
        self.attack = False
        self.x = def_x
        self.y = def_y
        self.shotFired = False
        self.grenadeThrown = False
        self.inJump = False
        self.jumpStarted = False
        self.lastDirection = 0
        self.ySpeed = 0
        self.alive = True
        self.ammunition = 9999
        self.explosives = 9999
        self.coins = 0
        self.health = 9999
        self.maxHealth = 9999
        self.animation_list_Idle = []
        self.index_Idle = 0
        self.updateTime = pygame.time.get_ticks()
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/IDLE00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Idle.append(img)

        self.animation_list_Run = []
        self.index_Run = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/RUN00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Run.append(img)

        self.animation_list_Attack = []
        self.index_Attack = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/ATTACK00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Attack.append(img)

        self.animation_list_Jump = []
        self.index_Jump = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/JUMP00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Jump.append(img)

        self.animation_list_Die = []
        self.index_Die = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/DIE00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Die.append(img)

        self.image = self.animation_list_Idle[self.index_Idle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update_animation(self, direction, flip, grenade, scroll, sound1):
        animation_refresh = 100
        attack_animation_refresh = 75

        if self.alive:

            if direction == 0 and self.inJump is False:
                self.image = self.animation_list_Idle[self.index_Idle]
                if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Idle += 1
                    if self.index_Idle == 6:
                        self.index_Idle = 0

            if (direction == 1 or direction == 2) and self.inJump is False:
                self.image = self.animation_list_Run[self.index_Run]
                if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Run += 1
                    if self.index_Run == 6:
                        self.index_Run = 0

            if self.attack and self.ammunition > 0 and self.inJump is False and self.shotFired is False:
                self.image = self.animation_list_Attack[self.index_Attack]
                if pygame.time.get_ticks() - self.updateTime > attack_animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Attack += 1
                    if self.index_Attack == 3:
                        if flip:
                            bullet = Bullet(self.rect.centerx + (-0.25 * self.rect.width), self.rect.centery, flip)
                        else:
                            bullet = Bullet(self.rect.centerx + (0.25 * self.rect.width), self.rect.centery, flip)
                        bullet_group.add(bullet)
                        sound1.play()
                    if self.index_Attack == 7:
                        self.index_Attack = 0
                        self.attack = False
                        self.shotFired = True
                        self.ammunition -= 1

            elif self.ammunition <= 0:
                self.attack = False
                self.shotFired = False

            if self.inJump:

                if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    if self.index_Jump < 6:
                        self.index_Jump += 1
                    self.image = self.animation_list_Jump[self.index_Jump]

            if grenade is True and self.attack is False and self.grenadeThrown is False and self.explosives > 0:
                grenade = Grenade(self.rect.centerx, self.rect.centery - 0.25 * self.rect.height, flip, scroll)
                grenade_group.add(grenade)
                self.grenadeThrown = True
                self.explosives -= 1

        if not self.alive:
            if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                self.updateTime = pygame.time.get_ticks()
                if self.index_Die < 6:
                    self.index_Die += 1
                self.image = self.animation_list_Die[self.index_Die]

    def move(self, direction, collision):
        dx = 0
        dy = 0
        shift = 0
        if self.alive:
            if direction == 1 and self.attack is False and self.inJump is False:
                dx = self.speed
                self.lastDirection = 1

            elif direction == 2 and self.attack is False and self.inJump is False:
                dx = (-self.speed)
                self.lastDirection = 2

            elif self.inJump:
                if self.jumpStarted is False:
                    self.ySpeed = -12

                if self.lastDirection == 1:
                    dx = int(0.5 * self.speed)

                elif self.lastDirection == 2:
                    dx = int(-0.5 * self.speed)

                elif self.lastDirection == 0:
                    dx = 0

                self.jumpStarted = True

            # apply gravity to the player
            self.ySpeed += grav_constant
            dy += self.ySpeed

            # check for player collisions
            for block in collision:
                if block[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                    dx = 0
                if block[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                    if self.ySpeed < 0:
                        self.ySpeed = 0
                        dy = block[1].bottom - self.rect.top
                    elif self.ySpeed >= 0:
                        self.ySpeed = 0
                        self.inJump = False
                        self.jumpStarted = False
                        dy = block[1].top - self.rect.bottom

            shift -= dx
            self.rect.y += dy

        return shift

    def hit(self, coin_sound, supply_sound):
        for explosion in explosions_group:
            if pygame.sprite.collide_rect(self, explosion):
                self.health -= explosion_dmg

        for sup in supplies_group:
            if pygame.sprite.collide_rect(self, sup):
                self.health += random.randrange(15, 45)
                if self.health > self.maxHealth:
                    self.health = self.maxHealth
                self.ammunition += random.randrange(12, 18)
                self.explosives += random.randrange(2, 5)
                self.coins += random.randrange(5, 15)
                sup.kill()
                supply_sound.play()

        for coin in coin_group:
            if pygame.sprite.collide_rect(self, coin):
                self.coins += 1
                coin.kill()
                coin_sound.play()

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.speed = 0

        if self.rect.y >= screen_height:
            self.health = 0
            self.alive = False

    def draw(self, game_window, flip):
        game_window.blit(pygame.transform.flip(self.image, flip, False), self.rect)

    @staticmethod
    def display_stuff(game_window, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        game_window.blit(img, (x, y))

    def apply_difficulty(self, dif):
        if dif == 1:
            self.maxHealth = 1000
            self.health = self.maxHealth
            self.ammunition = 60
            self.explosives = 15
        elif dif == 2:
            self.maxHealth = 250
            self.health = self.maxHealth
            self.ammunition = 20
            self.explosives = 5
        elif dif == 3:
            self.maxHealth = 150
            self.health = self.maxHealth
            self.ammunition = 10
            self.explosives = 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type, def_x, def_y, def_scale, def_speed, def_health, def_damage):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.scale = def_scale
        self.speed = def_speed
        self.x = def_x
        self.y = def_y
        self.attack = False
        self.lastDirection = 0
        self.ySpeed = 0
        self.alive = True
        self.health = def_health
        self.dmg = def_damage
        self.animation_list_Idle = []
        self.index_Idle = 0
        self.updateTime = pygame.time.get_ticks()
        self.direction = 0
        self.flip = False
        self.move_counter = 0
        self.idling = False
        self.idling_timer = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/IDLE00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Idle.append(img)

        self.animation_list_Run = []
        self.index_Run = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/RUN00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Run.append(img)

        self.animation_list_Attack = []
        self.index_Attack = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/ATTACK00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Attack.append(img)

        self.animation_list_Die = []
        self.index_Die = 0
        for i in range(7):
            img = pygame.image.load(f'resources/{self.char_type}/DIE00{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.animation_list_Die.append(img)

        self.image = self.animation_list_Idle[self.index_Idle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update_animation(self):
        animation_refresh = 100
        attack_animation_refresh = 50

        if self.alive:

            if self.direction == 0:
                self.image = self.animation_list_Idle[self.index_Idle]
                if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Idle += 1
                    if self.index_Idle == 6:
                        self.index_Idle = 0

            if self.direction == 1 or self.direction == 2:
                self.image = self.animation_list_Run[self.index_Run]
                if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Run += 1
                    if self.index_Run == 6:
                        self.index_Run = 0

            if self.attack:
                self.image = self.animation_list_Attack[self.index_Attack]
                if pygame.time.get_ticks() - self.updateTime > attack_animation_refresh:
                    self.updateTime = pygame.time.get_ticks()
                    self.index_Attack += 1
                    if self.index_Attack == 7:
                        self.index_Attack = 0

        if not self.alive:
            if pygame.time.get_ticks() - self.updateTime > animation_refresh:
                self.updateTime = pygame.time.get_ticks()
                if self.index_Die < 6:
                    self.index_Die += 1
                self.image = self.animation_list_Die[self.index_Die]

    def move(self, collision, shift):
        if self.alive:
            dx = 0
            dy = 0
            if self.direction == 1 and self.attack is False:
                dx = self.speed
                self.lastDirection = 1

            elif self.direction == 2 and self.attack is False:

                dx = (-self.speed)
                self.lastDirection = 2

            # apply gravity to the enemy
            self.ySpeed += grav_constant
            dy += self.ySpeed

            # check enemy for collisions
            for block in collision:
                if block[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                    if self.direction == 1:
                        dx = -10
                        self.direction = 0
                    elif self.direction == 2:
                        dx = 10
                        self.direction = 0
                    else:
                        dx = 0
                if block[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                    if self.ySpeed >= 0:
                        self.ySpeed = 0
                        dy = block[1].top - self.rect.bottom

            self.rect.x += dx + shift
            self.rect.y += dy
        else:
            self.rect.x += shift

    def hit(self):
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet):
                self.health -= bullet_dmg
                if self.alive is True:
                    bullet.kill()

        for explosion in explosions_group:
            if pygame.sprite.collide_rect(self, explosion):
                self.health -= explosion_dmg

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.speed = 0

    def draw(self, game_window):
        game_window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
