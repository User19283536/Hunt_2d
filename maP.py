import random
import playerCharacter
import enemieS
import coin
import supply
import pygame
import nextMaP

pygame.init()

nextMap_group = pygame.sprite.Group()

class Map:
    def __init__(self):
        self.world_blocks = []
        self.water_blocks = []
        self.misc_blocks = []

    def handle_map(self, data, player, objectImages_list, block_size):
        for y, total_row in enumerate(data):
            for x, blocks in enumerate(total_row):
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
                        player = playerCharacter.PlayerCharacter("character", x * block_size + 70, y * block_size - 5, 0.08,
                                                                5)
                    elif blocks == 16:
                        check = random.randint(1, 4)
                        if check == 1:
                            enemy = enemieS.Enemy("enemy01", x * block_size, y * block_size, 0.18, 2, 275, 15)
                        elif check == 2:
                            enemy = enemieS.Enemy("enemy02", x * block_size, y * block_size, 0.18, 2, 225, 17.5)
                        elif check == 3:
                            enemy = enemieS.Enemy("enemy03", x * block_size, y * block_size, 0.18, 2, 150, 22.5)
                        else:
                            enemy = enemieS.Enemy("enemy04", x * block_size, y * block_size, 0.08, 2, 100, 27.5)
                        playerCharacter.enemy_group.add(enemy)
                    elif blocks == 17:
                        supplies = supply.Supply(x * block_size + 30, y * block_size - 12)
                        playerCharacter.supplies_group.add(supplies)
                    elif blocks == 18:
                        coins = coin.Coin(x * block_size + 20, y * block_size - 10)
                        playerCharacter.coin_group.add(coins)
                    elif blocks == 20:
                        nextMap = nextMaP.NextMap(img, x * block_size, y * block_size, block_size)
                        nextMap_group.add(nextMap)
        return player

    def draw_level(self, GameWindow, screen_shift):
        for block in self.world_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])
        for block in self.water_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])
        for block in self.misc_blocks:
            block[1][0] += screen_shift
            GameWindow.blit(block[0], block[1])
