import pygame
import random

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
        self.grav_constant = 0.25
        self.sound_counter = 0
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
            self.ySpeed += self.grav_constant
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

    def hit(self, bullet_group, explosions_group, bullet_dmg, explosion_dmg):
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

    def attackPlayer(self, hurt_sound, player):
        if pygame.sprite.collide_mask(player, self) and player.alive is True:
            if self.alive is True:
                self.direction = 0
                self.attack = True
                if self.sound_counter % 30 == 0:
                    player.health -= self.dmg
                self.direction = self.lastDirection
                self.sound_counter += 1
                if self.sound_counter == 30:
                    hurt_sound.play()
                    self.sound_counter = 0

        elif player.alive is False:
            self.attack = False
            self.direction = 0
        else:
            self.attack = False
            self.direction = self.lastDirection


    def findPlayer(self, player, block_size):
            if player.alive and self.alive and self.rect.x - player.rect.x < 400 and abs(self.rect.y - player.rect.y) < 60:
                if player.rect.x >= self.rect.x:
                    self.direction = 1
                    self.flip = False
                if player.rect.x < self.rect.x:
                    self.direction = 2
                    self.flip = True
                if abs(self.rect.x - player.rect.x) <= 1:
                    self.direction = 0

            elif self.alive:
                if random.randint(1, 100) == 50 and self.idling is False:
                    self.idling = True
                    self.idling_timer = 50
                if self.idling is False:
                    self.move_counter += 1

                    if 4 * block_size <= self.move_counter < 8 * block_size:
                        self.direction = 2
                        self.flip = True

                    elif self.move_counter >= 8 * block_size:
                        self.direction = 1
                        self.flip = False
                        self.move_counter = 0
                else:
                    self.direction = 0
                    self.idling_timer -= 1
                    if self.idling_timer == 0:
                        self.idling = False
