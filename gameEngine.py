import pygame
import dynamicObjects
import random
import csv

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen_width = 1300
screen_height = 640
pygame.display.set_caption("Hunt2D")
GameWindow = pygame.display.set_mode((screen_width, screen_height))

map_number = 0
rows_number = 16
cols_number = 150
total_worldObjects = 21
block_size = screen_height // rows_number
dynamicObjects.block_size = block_size
dynamicObjects.screen_width = GameWindow.get_width()
dynamicObjects.screen_height = GameWindow.get_height()
screen_shift = 0
background_shift = 0
in_mainMenu = True
menu_difSelection = False
difficulty = 0
map_completed = False
showStatus_counter = 0
menu_screen_shift = 0
menu_shift_counter = 0
sound_counter = 0
objectImages_list = []
map_data = []

health = 0
ammo = 0
coins = 0
explosives = 0
player_max_health = 0

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setting framerate to 60 fps
FPS = 60
FrameRate = pygame.time.Clock()

# loading world object images to memory
for x in range(total_worldObjects):
    object_img = pygame.image.load(f'resources/level/tile/{x}.png')
    object_img = pygame.transform.scale(object_img, (block_size, block_size))
    objectImages_list.append(object_img)

# level data
for total_rows in range(rows_number):
    r = [-1] * cols_number
    map_data.append(r)

with open(f'level{map_number}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, total_rows in enumerate(reader, start=0):
        for y, world_block in enumerate(total_rows, start=0):
            map_data[x][y] = int(world_block)

background_image1 = pygame.image.load('resources/level/Background/wallpaper.png').convert_alpha()
background_image2 = pygame.image.load('resources/level/Background/wallpaper3.png').convert_alpha()
menu_wallpaper = pygame.image.load('resources/level/Background/wallpaper2.png').convert_alpha()
menu_text = pygame.image.load('resources/level/Background/MenuText.png').convert_alpha()
dif_text = pygame.image.load('resources/level/Background/DifText.png').convert_alpha()
death_text = pygame.image.load('resources/level/Background/DeathText.png').convert_alpha()
win_text = pygame.image.load('resources/level/Background/WinText.png').convert_alpha()

nextMap_group = pygame.sprite.Group()

# Creating default player character
player = dynamicObjects.PlayerCharacter("character", 90, 90, 0.08, 5)


def load_wallpaper():
    width = background_image1.get_width()
    global background_shift
    for x in range(-1, 5):
        if map_number % 2 == 0:
            GameWindow.blit(background_image1, ((x * width) - background_shift, 0))
        else:
            GameWindow.blit(background_image2, ((x * width) - background_shift, 0))

    if -3 * width > background_shift > -4 * width:
        background_shift = 0


def load_menu_background():
    global menu_screen_shift
    global menu_shift_counter
    menu_screen_shift -= 1

    width = background_image1.get_width()

    for x in range(5):
        GameWindow.blit(menu_wallpaper, ((width * x) + menu_screen_shift, 0))

    if -3 * width > menu_screen_shift > -4 * width:
        menu_screen_shift = 0

    if menu_difSelection is False:
        GameWindow.blit(menu_text, (0, 0))
    else:
        GameWindow.blit(dif_text, (0, 0))


def updateGameStatus(win_sound, death_sound):
    global showStatus_counter
    global map_number
    global ammo
    global health
    global explosives
    global coins
    global player_max_health
    if showStatus_counter > 100:
        if player.alive is False:
            GameWindow.blit(death_text, (0, 0))
            if showStatus_counter == 110:
                death_sound.play()

        else:
            GameWindow.blit(win_text, (0, 0))

            if showStatus_counter == 110:
                win_sound.play()
            if showStatus_counter == 350:
                ammo = player.ammunition
                explosives = player.explosives
                coins = player.coins
                health = player.health
                player_max_health = player.maxHealth
                map_number = map_number + 1
                restart_map()

    if player.alive is False:
        showStatus_counter += 1

    elif map_completed is True:
        showStatus_counter += 1


class Map:
    def __init__(self):
        self.world_blocks = []
        self.water_blocks = []
        self.misc_blocks = []

    def handle_map(self, data):
        global player
        for y, total_row in enumerate(data):
            for x, blocks in enumerate(total_row):
                global difficulty
                if blocks >= 0:
                    img = objectImages_list[blocks]
                    img_rect = img.get_rect()
                    img_rect.x = x * block_size
                    img_rect.y = y * block_size
                    block_param = (img, img_rect)
                    if 0 <= blocks <= 8:
                        self.world_blocks.append(block_param)
                    elif blocks == 9 or blocks == 10:
                        self.water_blocks.append(block_param)
                    elif 11 <= blocks <= 14 or blocks == 19:
                        self.misc_blocks.append(block_param)
                    elif blocks == 15:
                        player = dynamicObjects.PlayerCharacter("character", x * block_size + 70, y * block_size - 5, 0.08,
                                                                5)
                    elif blocks == 16:
                        check = random.randint(1, 4)
                        if check == 1:
                            enemy = dynamicObjects.Enemy("enemy01", x * block_size, y * block_size, 0.18, 2, 275, 15)
                        elif check == 2:
                            enemy = dynamicObjects.Enemy("enemy02", x * block_size, y * block_size, 0.18, 2, 225, 17.5)
                        elif check == 3:
                            enemy = dynamicObjects.Enemy("enemy03", x * block_size, y * block_size, 0.18, 2, 150, 22.5)
                        else:
                            enemy = dynamicObjects.Enemy("enemy04", x * block_size, y * block_size, 0.08, 2, 100, 27.5)
                        dynamicObjects.enemy_group.add(enemy)
                    elif blocks == 17:
                        supplies = dynamicObjects.Supply(x * block_size + 30, y * block_size - 12)
                        dynamicObjects.supplies_group.add(supplies)
                    elif blocks == 18:
                        coins = dynamicObjects.Coin(x * block_size + 20, y * block_size - 10)
                        dynamicObjects.coin_group.add(coins)
                    elif blocks == 20:
                        nextMap = NextMap(img, x * block_size, y * block_size)
                        nextMap_group.add(nextMap)

    def draw_level(self):
        for block in self.world_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])
        for block in self.water_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])
        for block in self.misc_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])


class NextMap(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + block_size // 2, y + (block_size - self.image.get_height()))

    def update(self):
        global map_completed
        self.rect.x += screen_shift
        if pygame.sprite.collide_rect(self, player):
            map_completed = True


level = Map()
level.handle_map(map_data)


def enemyAttack(hurt_sound):
    global sound_counter
    for enemy in dynamicObjects.enemy_group:
        if pygame.sprite.collide_mask(player, enemy) and player.alive is True:
            if enemy.alive is True:
                enemy.direction = 0
                enemy.attack = True
                if sound_counter % 30 == 0:
                    player.health -= enemy.dmg
                enemy.direction = enemy.lastDirection
                sound_counter += 1
                if sound_counter == 30:
                    hurt_sound.play()
                    sound_counter = 0


        elif player.alive is False:
            enemy.attack = False
            enemy.direction = 0
        else:
            enemy.attack = False
            enemy.direction = enemy.lastDirection


def enemyFindPlayer():
    for enemy in dynamicObjects.enemy_group:
        if player.alive and enemy.alive and enemy.rect.x - player.rect.x < 400 and abs(
                enemy.rect.y - player.rect.y) < 60:
            if player.rect.x >= enemy.rect.x:
                enemy.direction = 1
                enemy.flip = False
            if player.rect.x < enemy.rect.x:
                enemy.direction = 2
                enemy.flip = True
            if abs(enemy.rect.x - player.rect.x) <= 1:
                enemy.direction = 0

        elif enemy.alive:
            if random.randint(1, 100) == 50 and enemy.idling is False:
                enemy.idling = True
                enemy.idling_timer = 50
            if enemy.idling is False:
                enemy.move_counter += 1

                if 4 * block_size <= enemy.move_counter < 8 * block_size:
                    enemy.direction = 2
                    enemy.flip = True

                elif enemy.move_counter >= 8 * block_size:
                    enemy.direction = 1
                    enemy.flip = False
                    enemy.move_counter = 0
            else:
                enemy.direction = 0
                enemy.idling_timer -= 1
                if enemy.idling_timer == 0:
                    enemy.idling = False


def restart_map():
    global map_completed
    global showStatus_counter
    global player
    global level
    global background_shift
    global health
    global explosives
    global ammo
    global coins
    global player_max_health
    background_shift = 0
    dynamicObjects.bullet_group.empty()
    dynamicObjects.grenade_group.empty()
    dynamicObjects.enemy_group.empty()
    dynamicObjects.explosions_group.empty()
    dynamicObjects.supplies_group.empty()
    dynamicObjects.coin_group.empty()
    nextMap_group.empty()
    player.alive = True
    showStatus_counter = 0

    with open(f'level{map_number}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                map_data[x][y] = int(tile)

    level = Map()
    level.handle_map(map_data)
    if map_completed is True:
        player.health = health
        player.ammunition = ammo
        player.explosives = explosives
        player.coins = coins
        player.maxHealth = player_max_health
    map_completed = False


def main():
    global in_mainMenu
    global screen_shift
    global background_shift
    global menu_difSelection
    global difficulty

    pygame.mixer.music.load('resources/audio/GameTune.mp3')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, 0.0, 9000)

    shot_effect = pygame.mixer.Sound('resources/audio/gunshot.mp3')
    shot_effect.set_volume(0.3)
    explosion_effect = pygame.mixer.Sound('resources/audio/explosion.mp3')
    explosion_effect.set_volume(0.3)

    jump_effect = pygame.mixer.Sound('resources/audio/jump.wav')
    jump_effect.set_volume(0.3)

    coin_effect = pygame.mixer.Sound('resources/audio/coin.wav')
    coin_effect.set_volume(0.3)

    chest_effect = pygame.mixer.Sound('resources/audio/chest.wav')
    chest_effect.set_volume(0.3)

    win_effect = pygame.mixer.Sound('resources/audio/win.wav')
    win_effect.set_volume(0.3)

    death_effect = pygame.mixer.Sound('resources/audio/death.wav')
    death_effect.set_volume(0.3)

    hurt_effect = pygame.mixer.Sound('resources/audio/hurt.wav')
    hurt_effect.set_volume(0.3)

    button_effect = pygame.mixer.Sound('resources/audio/menu_click.wav')
    button_effect.set_volume(0.3)

    movement_direction = 0
    flip = False
    grenade = False
    font = pygame.font.Font('resources/font/Arcade.ttf', 30)
    run = True
    purchase_made = False

    while run:
        FrameRate.tick(FPS)

        if not in_mainMenu:
            load_wallpaper()
            level.draw_level()

            for enemy in dynamicObjects.enemy_group:
                enemy.update_animation()
                enemy.move(level.world_blocks, screen_shift)
                enemy.hit()
                dynamicObjects.Enemy.draw(enemy, GameWindow)

            enemyAttack(hurt_effect)
            enemyFindPlayer()

            dynamicObjects.bullet_group.update(level.world_blocks)
            dynamicObjects.bullet_group.draw(GameWindow)

            dynamicObjects.grenade_group.update(level.world_blocks, screen_shift, explosion_effect)
            dynamicObjects.grenade_group.draw(GameWindow)

            dynamicObjects.explosions_group.update(screen_shift)
            dynamicObjects.explosions_group.draw(GameWindow)

            dynamicObjects.supplies_group.update(screen_shift)
            dynamicObjects.supplies_group.draw(GameWindow)

            dynamicObjects.coin_group.update(screen_shift)
            dynamicObjects.coin_group.draw(GameWindow)

            nextMap_group.draw(GameWindow)
            nextMap_group.update()

            player.update_animation(movement_direction, flip, grenade, screen_shift, shot_effect)
            screen_shift = player.move(movement_direction, level.world_blocks)
            background_shift -= screen_shift // 2
            player.hit(coin_effect, chest_effect)
            player.draw(GameWindow, flip)
            ammo_text = f'Ammunition {player.ammunition}'
            player.display_stuff(GameWindow, ammo_text, font, WHITE, 20, 10)
            expl_text = f'Explosives {player.explosives}'
            player.display_stuff(GameWindow, expl_text, font, WHITE, 220, 10)
            score_text = f'Coins {player.coins}'
            player.display_stuff(GameWindow, score_text, font, WHITE, 410, 10)
            health_text = f'Health {int(player.health)}'
            if float(player.health / player.maxHealth) >= 0.5:
                player.display_stuff(GameWindow, health_text, font, WHITE, 540, 10)
            elif float(player.health / player.maxHealth) >= 0.25:
                player.display_stuff(GameWindow, health_text, font, ORANGE, 540, 10)
            elif float(player.health / player.maxHealth) > 0:
                player.display_stuff(GameWindow, health_text, font, RED, 540, 10)
            elif float(player.health / player.maxHealth) == 0:
                player.display_stuff(GameWindow, 'Dead', font, RED, 540, 10)
        updateGameStatus(win_effect, death_effect)

        if in_mainMenu:
            load_menu_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and player.alive and player.inJump is False and player.attack is False:
                    flip = False
                    movement_direction = 1

                if event.key == pygame.K_a and player.alive and player.inJump is False and player.attack is False:
                    flip = True
                    movement_direction = 2

                if event.key == pygame.K_SPACE and player.alive and player.inJump is False:
                    player.attack = True
                    player.shotFired = False

                if event.key == pygame.K_q and player.alive and player.inJump is False and player.attack is False:
                    grenade = True

                if event.key == pygame.K_w and player.alive and player.inJump is False and player.attack is False:
                    player.inJump = True
                    jump_effect.play()

                if event.key == pygame.K_u and purchase_made is False:
                    if player.coins >= 10:
                        player.ammunition += 6
                        player.coins -= 10
                    purchase_made = True

                if event.key == pygame.K_i and purchase_made is False:
                    if player.coins >= 10:
                        player.explosives += 2
                        player.coins -= 10
                    purchase_made = True

                if event.key == pygame.K_p and purchase_made is False:
                    if player.coins >= 15:
                        dynamicObjects.bullet_dmg += 10
                        player.coins -= 15
                    purchase_made = True

                if event.key == pygame.K_v and in_mainMenu is True:
                    menu_difSelection = True
                    button_effect.play()

                if event.key == pygame.K_1 and menu_difSelection is True:
                    player.apply_difficulty(1)
                    menu_difSelection = False
                    in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_2 and menu_difSelection is True:
                    player.apply_difficulty(2)
                    menu_difSelection = False
                    in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_3 and menu_difSelection is True:
                    player.apply_difficulty(3)
                    menu_difSelection = False
                    in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_ESCAPE and in_mainMenu is False:
                    in_mainMenu = True
                    button_effect.play()
                    restart_map()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    movement_direction = 0
                if event.key == pygame.K_a:
                    movement_direction = 0

                if event.key == pygame.K_SPACE:
                    player.shotFired = False

                if event.key == pygame.K_q:
                    grenade = False
                    player.grenadeThrown = False

                if event.key == pygame.K_u and purchase_made is True:
                    purchase_made = False

                if event.key == pygame.K_i and purchase_made is True:
                    purchase_made = False

                if event.key == pygame.K_p and purchase_made is True:
                    purchase_made = False

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
