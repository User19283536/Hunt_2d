import pygame
import playerCharacter
import csv
import enemieS
import maP
import controlVariables

pygame.init()
pygame.font.init()
pygame.mixer.init()

newGame = controlVariables.gameStatus()

pygame.display.set_caption("Hunt2D")
GameWindow = pygame.display.set_mode((newGame.screen_width, newGame.screen_height))

background_image1 = pygame.image.load('resources/level/Background/wallpaper.png').convert_alpha()
background_image2 = pygame.image.load('resources/level/Background/wallpaper3.png').convert_alpha()
menu_wallpaper = pygame.image.load('resources/level/Background/wallpaper2.png').convert_alpha()
menu_text = pygame.image.load('resources/level/Background/MenuText.png').convert_alpha()
dif_text = pygame.image.load('resources/level/Background/DifText.png').convert_alpha()
death_text = pygame.image.load('resources/level/Background/DeathText.png').convert_alpha()
win_text = pygame.image.load('resources/level/Background/WinText.png').convert_alpha()

# Setting framerate to 60 fps
FPS = 60
FrameRate = pygame.time.Clock()

# loading world object images to memory
for x in range(newGame.total_worldObjects):
    object_img = pygame.image.load(f'resources/level/tile/{x}.png')
    object_img = pygame.transform.scale(object_img, (newGame.block_size, newGame.block_size))
    newGame.objectImages_list.append(object_img)

# level data
for total_rows in range(newGame.rows_number):
    r = [-1] * newGame.cols_number
    newGame.map_data.append(r)

with open(f'level{newGame.map_number}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, total_rows in enumerate(reader, start=0):
        for y, world_block in enumerate(total_rows, start=0):
            newGame.map_data[x][y] = int(world_block)


# Creating default player character
player = playerCharacter.PlayerCharacter("character", 90, 90, 0.08, 5)


def load_wallpaper():
    width = background_image1.get_width()

    for x in range(-1, 5):
        if newGame.map_number % 2 == 0:
            GameWindow.blit(background_image1, ((x * width) - newGame.background_shift, 0))
        else:
            GameWindow.blit(background_image2, ((x * width) - newGame.background_shift, 0))

    if -3 * width > newGame.background_shift > -4 * width:
        newGame.background_shift = 0


def load_menu_background():
    newGame.menu_screen_shift -= 1

    width = background_image1.get_width()

    for x in range(5):
        GameWindow.blit(menu_wallpaper, ((width * x) + newGame.menu_screen_shift, 0))

    if -3 * width > newGame.menu_screen_shift > -4 * width:
        newGame.menu_screen_shift = 0

    if newGame.menu_difSelection is False:
        GameWindow.blit(menu_text, (0, 0))
    else:
        GameWindow.blit(dif_text, (0, 0))


def updateGameStatus(win_sound, death_sound):


    if newGame.showStatus_counter > 100:
        if player.alive is False:
            GameWindow.blit(death_text, (0, 0))
            if newGame.showStatus_counter == 110:
                death_sound.play()

        else:
            GameWindow.blit(win_text, (0, 0))

            if newGame.showStatus_counter == 110:
                win_sound.play()
            if newGame.showStatus_counter == 350:
                newGame.ammo = player.ammunition
                newGame.explosives = player.explosives
                newGame.coins = player.coins
                newGame.health = player.health
                newGame.player_max_health = player.maxHealth
                newGame.map_number = newGame.map_number + 1
                restart_map()

    if player.alive is False:
        newGame.showStatus_counter += 1

    elif newGame.map_completed is True:
        newGame.showStatus_counter += 1


level = maP.Map()
player = level.handle_map(newGame.map_data, player, newGame.objectImages_list, newGame.block_size)


def restart_map():
    global level
    global player
    newGame.background_shift = 0
    playerCharacter.bullet_group.empty()
    playerCharacter.grenade_group.empty()
    playerCharacter.enemy_group.empty()
    playerCharacter.explosions_group.empty()
    playerCharacter.supplies_group.empty()
    playerCharacter.coin_group.empty()
    maP.nextMap_group.empty()
    if player.alive is False:
        newGame.bullet_dmg = 50
    player.alive = True
    newGame.showStatus_counter = 0


    with open(f'level{newGame.map_number}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                newGame.map_data[x][y] = int(tile)

    level = maP.Map()
    player = level.handle_map(newGame.map_data, player, newGame.objectImages_list, newGame.block_size)
    if newGame.map_completed is True:
        player.health = newGame.health
        player.ammunition = newGame.ammo
        player.explosives = newGame.explosives
        player.coins = newGame.coins
        player.maxHealth = newGame.player_max_health
    newGame.map_completed = False


def main():


    explosion_dmg = 20

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

        if not newGame.in_mainMenu:
            load_wallpaper()
            level.draw_level(GameWindow, newGame.screen_shift)

            for enemy in playerCharacter.enemy_group:
                enemy.update_animation()
                enemy.move(level.world_blocks, newGame.screen_shift)
                enemy.hit(playerCharacter.bullet_group, playerCharacter.explosions_group, newGame.bullet_dmg, explosion_dmg)
                enemieS.Enemy.draw(enemy, GameWindow)

            for enemy in playerCharacter.enemy_group:
                enemy.attackPlayer(hurt_effect, player)
                enemy.findPlayer(player, newGame.block_size)

            for sign in maP.nextMap_group:
                if sign.completed is True:
                    newGame.map_completed = True

            playerCharacter.bullet_group.update(level.world_blocks, newGame.screen_width)
            playerCharacter.bullet_group.draw(GameWindow)

            playerCharacter.grenade_group.update(level.world_blocks, newGame.screen_shift, explosion_effect, playerCharacter.explosions_group)
            playerCharacter.grenade_group.draw(GameWindow)

            playerCharacter.explosions_group.update(newGame.screen_shift)
            playerCharacter.explosions_group.draw(GameWindow)

            playerCharacter.supplies_group.update(newGame.screen_shift)
            playerCharacter.supplies_group.draw(GameWindow)

            playerCharacter.coin_group.update(newGame.screen_shift)
            playerCharacter.coin_group.draw(GameWindow)

            maP.nextMap_group.draw(GameWindow)
            maP.nextMap_group.update(newGame.screen_shift, player)

            player.update_animation(movement_direction, flip, grenade, newGame.screen_shift, shot_effect)
            newGame.screen_shift = player.move(movement_direction, level.world_blocks)
            newGame.background_shift -= newGame.screen_shift // 2
            player.hit(coin_effect, chest_effect, explosion_dmg)
            player.draw(GameWindow, flip)
            ammo_text = f'Ammunition {player.ammunition}'
            player.display_stuff(GameWindow, ammo_text, font, newGame.WHITE, 20, 10)
            expl_text = f'Explosives {player.explosives}'
            player.display_stuff(GameWindow, expl_text, font, newGame.WHITE, 220, 10)
            score_text = f'Coins {player.coins}'
            player.display_stuff(GameWindow, score_text, font, newGame.WHITE, 410, 10)
            health_text = f'Health {int(player.health)}'
            if float(player.health / player.maxHealth) >= 0.5:
                player.display_stuff(GameWindow, health_text, font, newGame.WHITE, 540, 10)
            elif float(player.health / player.maxHealth) >= 0.25:
                player.display_stuff(GameWindow, health_text, font, newGame.ORANGE, 540, 10)
            elif float(player.health / player.maxHealth) > 0:
                player.display_stuff(GameWindow, health_text, font, newGame.RED, 540, 10)
            elif float(player.health / player.maxHealth) == 0:
                player.display_stuff(GameWindow, 'Dead', font, newGame.RED, 540, 10)
        updateGameStatus(win_effect, death_effect)

        if newGame.in_mainMenu:
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
                        newGame.bullet_dmg += 10
                        player.coins -= 15
                    purchase_made = True

                if event.key == pygame.K_v and newGame.in_mainMenu is True:
                    newGame.menu_difSelection = True
                    button_effect.play()

                if event.key == pygame.K_1 and newGame.menu_difSelection is True:
                    player.apply_difficulty(1)
                    newGame.menu_difSelection = False
                    newGame.in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_2 and newGame.menu_difSelection is True:
                    player.apply_difficulty(2)
                    newGame.menu_difSelection = False
                    newGame.in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_3 and newGame.menu_difSelection is True:
                    player.apply_difficulty(3)
                    newGame.menu_difSelection = False
                    newGame.in_mainMenu = False
                    button_effect.play()

                if event.key == pygame.K_ESCAPE and newGame.in_mainMenu is False:
                    newGame.in_mainMenu = True
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
