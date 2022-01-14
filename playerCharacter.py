import pygame
import bullet
import random
import grenadeS
import controlVariables

pygame.init()
pygame.font.init()

newGame = controlVariables.gameStatus()
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
                            projectile = bullet.Bullet(self.rect.centerx + (-0.25 * self.rect.width), self.rect.centery, flip)
                        else:
                            projectile = bullet.Bullet(self.rect.centerx + (0.25 * self.rect.width), self.rect.centery, flip)
                        bullet_group.add(projectile)
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
                grenade = grenadeS.Grenade(self.rect.centerx, self.rect.centery - 0.25 * self.rect.height, flip, scroll, newGame.grav_constant)
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
            self.ySpeed += newGame.grav_constant
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

    def hit(self, coin_sound, supply_sound, explosion_dmg):
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

        if self.rect.y >= newGame.screen_height:
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


