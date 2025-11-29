import pygame
from clases.terrain import Terrain
from clases.player import Player
from clases.fruits import Fruits

terrain_pos = (96, 0)
terrain_extra_pos = (144, 0)
solids_pos = (192, 0)
player_start = (112, 16)
tile_multiplier = 16
tile_size = 32

scene_terrain = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 2, 2, 13, 5, 12, 2, 2, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 2, 13, 5, 5, 5, 5, 5, 5, 5, 12, 2, 3, 0, 0, 0],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
                [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9],]

fruit_pos = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

class Start:
    def __init__(self, screen):
        self.collectables = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.background = pygame.image.load("assets/Background/Blue.png").convert()
        _, _, width, height = self.background.get_rect()
        #self.terrain = []
        self.tiles = []

        screenW, screenH = screen.get_size()

        for i in range(screenW // width + 1):
            for j in range(screenH // height + 1):
                pos = (i * width, j * height)
                self.tiles.append(pos)

        for row in range(len(scene_terrain)):
            for col in range(len(scene_terrain[row])):
                tile_id = scene_terrain[row][col]
                if tile_id == 0:
                    continue
                
                pos_x = col * tile_size
                pos_y = row * tile_size

                tile_offset_x, tile_offset_y = self.getTilePosition(tile_id)

                # tile_offset_x = terrain_pos[0] + tile_multiplier * ((tile_id - 1) % 3)
                # tile_offset_y = terrain_pos[1] + tile_multiplier * ((tile_id - 1) // 3)
                
                # self.terrain.append(
                #     Terrain(pos_x, pos_y, tile_size, tile_offset_x, tile_offset_y)
                # )
                terrain = Terrain(pos_x, pos_y, tile_size, tile_offset_x, tile_offset_y)
                self.platform_list.add(terrain)
                self.all_sprites.add(terrain)
        
        for row in range(len(fruit_pos)):
            for col in range(len(fruit_pos[row])):
                tile_id = fruit_pos[row][col]
                if tile_id == 0:
                    continue
                
                fruit = Fruits('Apple')
                
                fruit.rect.x = (col * tile_size) - (fruit.rect.width//4)
                fruit.rect.y = (row * tile_size) - (fruit.rect.height//4)

                self.collectables.add(fruit)
                self.all_sprites.add(fruit)
    
    def getTilePosition(self, tile_id):
        tile_offset_x = tile_offset_y = 0
        match tile_id:
            case 1:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
            case 2:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
            case 3:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
            case 4:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
            case 5:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
            case 6:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
            case 7:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
            case 8:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
            case 9:
                tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
                tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
            case 10:
                tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 0)
                tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 0)
            case 11:
                tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 1)
                tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 0)
            case 12:
                tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 0)
                tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 1)
            case 13:
                tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 1)
                tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 1)
        return tile_offset_x, tile_offset_y
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        for tile in self.tiles:
            screen.blit(self.background, tile)
        #self.platform_list.draw(screen)
        self.all_sprites.draw(screen)
    
    def update(self):
        self.all_sprites.update()
    
    def clear(self):
        self.tiles.clear()
        #self.platform_list.empty()
        self.all_sprites.empty()