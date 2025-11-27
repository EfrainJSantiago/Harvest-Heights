import pygame
#from clases.enemy import Enemy
from clases.terrain import Terrain
from clases.fruits import Fruits
import random

class Scene:
    def __init__(self, scene_values: list):
        #self.enemy_list = pygame.sprite.Group()
        self.collectables_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.terrain_pos = scene_values['terrain_pos']
        self.terrain_extra_pos = scene_values['terrain_extra_pos']
        self.solid_pos = scene_values['solids_pos']
        self.tile_mult = scene_values['tile_multiplier']
        self.tile_size = scene_values['tile_size']
        self.border1 = scene_values['border1']
        self.border1 = scene_values['border1_extras']
        self.border2 = scene_values['border2']
        self.border1 = scene_values['border2_extras']
        self.background = pygame.image.load("assets/Background/" + scene_values['background_color'] + ".png").convert()
        self.tiles = []
        self.scene_terrain = scene_values['scene_terrain']
        self.scene_collectables = scene_values['scene_collectables']
        self.scene_enemies = scene_values['scene_enemies']
        self.respawn_point = None

        if scene_values['start']:
            self.respawn_point = scene_values['start']
        elif scene_values['checkpoint']:
            self.respawn_point = scene_values['checkpoint']

        # 19 tile width, 13 tile height
    
    def constructScene(self, screen):
        self.background = pygame.image.load("assets/Background/Blue.png").convert()
        _, _, width, height = self.background.get_rect()

        for i in range(screen.width // width + 1):
            for j in range(screen.height // height + 1):
                pos = (i * width, j * height)
                self.tiles.append(pos)

        for row in range(len(self.scene_terrain)):
            for col in range(len(self.scene_terrain[row])):
                tile_id = self.scene_terrain[row][col]
                if tile_id == 0:
                    continue
                
                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                tile_offset_x, tile_offset_y = self.getTilePosition(tile_id)

                terrain = Terrain(pos_x, pos_y, self.tile_size, tile_offset_x, tile_offset_y)
                
                self.platform_list.add(terrain)
                self.all_sprites.add(terrain)
        
        for row in range(len(self.scene_collectables)):
            for col in range(len(self.scene_collectables[row])):
                tile_id = self.scene_collectables[row][col]
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
        return self.all_sprites.copy()
    
    def getTilePosition(self, tile_id):
        tile_offset_x = tile_offset_y = 0
        match tile_id:
            case 1:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 0)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 0)
            case 2:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 1)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 0)
            case 3:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 2)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 0)
            case 4:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 0)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 1)
            case 5:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 1)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 1)
            case 6:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 2)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 1)
            case 7:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 0)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 2)
            case 8:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 1)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 2)
            case 9:
                tile_offset_x = self.terrain_pos[0] + (self.tile_mult * 2)
                tile_offset_y = self.terrain_pos[1] + (self.tile_mult * 2)
            case 10:
                tile_offset_x = self.terrain_extra_pos[0] + (self.tile_mult * 0)
                tile_offset_y = self.terrain_extra_pos[1] + (self.tile_mult * 0)
            case 11:
                tile_offset_x = self.terrain_extra_pos[0] + (self.tile_mult * 1)
                tile_offset_y = self.terrain_extra_pos[1] + (self.tile_mult * 0)
            case 12:
                tile_offset_x = self.terrain_extra_pos[0] + (self.tile_mult * 0)
                tile_offset_y = self.terrain_extra_pos[1] + (self.tile_mult * 1)
            case 13:
                tile_offset_x = self.terrain_extra_pos[0] + (self.tile_mult * 1)
                tile_offset_y = self.terrain_extra_pos[1] + (self.tile_mult * 1)
        return tile_offset_x, tile_offset_y

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