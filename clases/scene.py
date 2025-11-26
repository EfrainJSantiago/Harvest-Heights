import pygame
#from clases.enemy import Enemy
from clases.terrain import Terrain
from clases.fruits import Fruits
import random

class Scene:
    def __init__(self, background, terrain_pos: tuple,
                 terrain_extra_pos: tuple, solid_pos: tuple, tile_mult: tuple,
                 tile_size: tuple, border1: tuple, border1_extras: tuple, border2: tuple,
                 border2_extras: tuple):
        #self.enemy_list = pygame.sprite.Group()
        self.collectables_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.terrain_pos = terrain_pos
        self.terrain_extra_pos = terrain_extra_pos
        self.solid_pos = solid_pos
        self.tile_mult = tile_mult
        self.tile_size = tile_size
        self.border1 = border1
        self.border2 = border2
        self.background = pygame.image.load("assets/Background/" + background + ".png").convert()
        self.tiles = []

        # 19 tile width, 13 tile height
    
    def constructScene(self, screen, scene_terrain, scene_collectables):
        self.background = pygame.image.load("assets/Background/Blue.png").convert()
        _, _, width, height = self.background.get_rect()

        for i in range(screen.width // width + 1):
            for j in range(screen.height // height + 1):
                pos = (i * width, j * height)
                self.tiles.append(pos)

        for row in range(len(scene_terrain)):
            for col in range(len(scene_terrain[row])):
                tile_id = scene_terrain[row][col]
                if tile_id == 0:
                    continue
                
                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                tile_offset_x, tile_offset_y = self.getTilePosition(tile_id)

                terrain = Terrain(pos_x, pos_y, self.tile_size, tile_offset_x, tile_offset_y)
                
                self.platform_list.add(terrain)
                self.all_sprites.add(terrain)
        
        for row in range(len(scene_collectables)):
            for col in range(len(scene_collectables[row])):
                tile_id = scene_collectables[row][col]
                if tile_id == 0:
                    continue
                
                fruit = Fruits('Apple')
                
                fruit.rect.x = (col * self.tile_size) - (fruit.rect.width//4)
                fruit.rect.y = (row * self.tile_size) - (fruit.rect.height//4)

                self.collectables_list.add(fruit)
                self.all_sprites.add(fruit)
    
    def getCollectables(self):
        return self.collectables_list
    
    def getPlatforms(self):
        return self.platform_list
    
    def getSprites(self):
        return self.all_sprites

    def resetScene(self, scene, scene_terrain, scene_collectables):
        self.clear()
        self.constructScene(scene, scene_terrain, scene_collectables)
    #     self.player.rect.x = 0
    #     self.player.rect.y = 0
    #     self.enemy_list.empty()
    #     self.all_sprites.empty()
    #     self.platform_list.empty()
    #     self.startGame(width, height)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for tile in self.tiles:
            screen.blit(self.background, tile)
        #self.platform_list.draw(screen)
        self.all_sprites.draw(screen)
    
    def update(self):
        self.all_sprites.update()

    # def checkFinished(self):
    #     if len(self.enemy_list) == 0:
    #         return True
    #     else:
    #         return False

    # def eat(self):
    #     sprite_hit = pygame.sprite.spritecollide(self.player, self.enemy_list, True)
    #     point = 0
    #     if sprite_hit:
    #         point = point + 1
    #     return point

    # def collide_big_enemy(self, big_enemy):
    #     if big_enemy.colliderect(self.player.rect):
    #         return True
    #     return False

    def clear(self):
        self.tiles.clear()
        #self.platform_list.empty()
        self.all_sprites.empty()