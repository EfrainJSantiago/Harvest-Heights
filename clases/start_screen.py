import pygame
from clases.terrain import Terrain
from clases.player import Player

terrain_pos = (96, 0)
tile_multiplier = 16
ROWS = 19
COLS = 13
tile_size = 32

scene_terrain = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3],
                [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 5, 6],
                [4, 5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 5, 5, 6],
                [4, 5, 5, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 5, 5, 6],
                [4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6],]

class Start:
    def __init__(self, screen):
        #self.terrain = pygame.image.load("assets/Terrain/Terrain (16x16).png").convert()
        self.all_sprites = pygame.sprite.Group()
        self.background = pygame.image.load("assets/Background/Blue.png").convert()
        _, _, width, height = self.background.get_rect()
        self.terrain = []
        self.tiles = []
        #self.player = Player(screen.get_size())

        for i in range(screen.width // width + 1):
            for j in range(screen.height // height + 1):
                pos = (i * width, j * height)
                self.tiles.append(pos)

        # row = 0
        # col = 0

        # for i in range(-screen.width // tile_size, (screen.width * 2) // tile_size):
        #     for j in range(-screen.height // tile_size, (screen.height * 2) // tile_size):
        #         if scene_terrain[row][col] == 0:
        #             continue
        #         elif scene_terrain[row][col] == 1:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 0), terrain_pos[1] + (tile_multiplier * 0)))
        #         elif scene_terrain[row][col] == 2:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 1), terrain_pos[1] + (tile_multiplier * 0)))
        #         elif scene_terrain[row][col] == 3:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 2), terrain_pos[1] + (tile_multiplier * 0)))
        #         elif scene_terrain[row][col] == 4:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 0), terrain_pos[1] + (tile_multiplier * 1)))
        #         elif scene_terrain[row][col] == 5:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 1), terrain_pos[1] + (tile_multiplier * 1)))
        #         elif scene_terrain[row][col] == 6:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 2), terrain_pos[1] + (tile_multiplier * 1)))
        #         elif scene_terrain[row][col] == 7:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 0), terrain_pos[1] + (tile_multiplier * 2)))
        #         elif scene_terrain[row][col] == 8:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 1), terrain_pos[1] + (tile_multiplier * 2)))
        #         elif scene_terrain[row][col] == 9:
        #             self.terrain.append(Terrain(i * tile_size, j * tile_size, tile_size, terrain_pos[0] + (tile_multiplier * 2), terrain_pos[1] + (tile_multiplier * 2)))
        #         col += 1
        #     col = 0
        #     row += 1
        for row in range(len(scene_terrain)):
            for col in range(len(scene_terrain[row])):
                tile_id = scene_terrain[row][col]
                if tile_id == 0:
                    continue
                
                world_x = col * tile_size
                world_y = row * tile_size
                
                tile_offset_x = terrain_pos[0] + tile_multiplier * ((tile_id - 1) % 3)
                tile_offset_y = terrain_pos[1] + tile_multiplier * ((tile_id - 1) // 3)
                
                self.terrain.append(
                    Terrain(world_x, world_y, tile_size, tile_offset_x, tile_offset_y)
                )

        #self.all_sprites.add(self.player)
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        for tile in self.tiles:
            screen.blit(self.background, tile)
        for tile in self.terrain:
            tile.draw(screen)
        #self.all_sprites.draw(screen)
    
    def clear(self):
        self.tiles.clear()
        for tile in self.terrain:
            tile.kill()
        self.terrain.clear()
        #self.all_sprites.clear()