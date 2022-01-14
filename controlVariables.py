import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()


class gameStatus:
    def __init__(self):
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.screen_width = 1300
        self.screen_height = 640
        self.map_number = 0
        self.rows_number = 16
        self.cols_number = 150
        self.total_worldObjects = 21
        self.block_size = self.screen_height // self.rows_number
        self.grav_constant = 0.25
        self.screen_shift = 0
        self.background_shift = 0
        self.in_mainMenu = True
        self.menu_difSelection = False
        self.difficulty = 0
        self.map_completed = False
        self.showStatus_counter = 0
        self.menu_screen_shift = 0
        self.menu_shift_counter = 0
        self.health = 0
        self.ammo = 0
        self.coins = 0
        self.explosives = 0
        self.player_max_health = 0
        self.objectImages_list = []
        self.map_data = []
        self.bullet_dmg = 50
