import pygame
#from clases.enemy import Enemy
from clases.terrain import Terrain
from clases.fruits import Fruits
from clases.enemy_types import *
import random

class Scene:
    def __init__(self, scene_values: list):
        # Listas de sprites
        self.enemy_list = pygame.sprite.Group()
        self.collectables_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.semisolid_list = pygame.sprite.Group()

        # Guarda los valores de la escena
        self.terrain_pos = scene_values['terrain_pos']
        self.terrain_extra_pos = scene_values['terrain_extra_pos']
        self.decor_pos = scene_values['decor_pos']
        self.decor_type = scene_values['decor_type']
        self.semisolid_pos = scene_values['semisolid_pos']
        self.tile_mult = scene_values['tile_multiplier']
        self.tile_size = scene_values['tile_size']
        self.fruit_palette = scene_values['fruit_palette']
        self.background = pygame.image.load("assets/Background/" + scene_values['background_color'] + ".png").convert()
        self.scene_terrain = scene_values['scene_terrain']
        self.scene_decor = scene_values['scene_decor']
        self.scene_semisolid = scene_values['scene_semisolid']
        self.scene_collectables = scene_values['scene_collectables']
        self.scene_enemies = scene_values['scene_enemies']

        # Obtiene el punto de partida de la escena
        self.respawn_point = None
        if scene_values['start'] != None:
            self.respawn_point = scene_values['start']
        elif scene_values['checkpoint'] != None:
            self.respawn_point = scene_values['checkpoint']
        else:
            self.respawn_point = (32, 96)
        
        # Obtiene el punto de final de la escena si existe
        self.endpoint = None
        if scene_values['end'] != None:
            self.endpoint = scene_values['end']
        
        # Variable del background
        self.tiles = []
    
    def constructScene(self, screenW, screenH):
        """ Construye la escena del nivel.
        """
        self.tiles.clear()
        _, _, width, height = self.background.get_rect()

        # Añade el background a la escena
        for i in range(screenW // width + 1):
            for j in range(screenH // height + 1):
                pos = (i * width, j * height)
                self.tiles.append(pos)
        
        tile_offset_x, tile_offset_y = 0, 0

        # Añade el terreno a la escena
        for row in range(len(self.scene_terrain)):
            for col in range(len(self.scene_terrain[row])):
                tile_id = self.scene_terrain[row][col]
                if tile_id == 0:
                    continue
                
                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                if tile_id in range(1, 10):
                    tile_offset_x, tile_offset_y = self.getTilePosition(self.terrain_pos, tile_id, 3)
                elif tile_id in range(10, 14):
                    tile_offset_x, tile_offset_y = self.getTilePosition(self.terrain_extra_pos, tile_id, 2)

                terrain = Terrain(pos_x, pos_y, self.tile_size, tile_offset_x, tile_offset_y)
                
                self.platform_list.add(terrain)
        
        # Añade los bloques decorativos a la escena
        for row in range(len(self.scene_decor)):
            for col in range(len(self.scene_decor[row])):
                tile_id = self.scene_decor[row][col]
                if tile_id == 0:
                    continue

                decor_pos = list(self.decor_pos)

                match self.decor_type:
                    case 'brown':
                        pass
                    case 'gray':
                        decor_pos[1] += 64
                    case 'orange':
                        decor_pos[1] += 128
                    case 'gold':
                        decor_pos[1] += 128
                        decor_pos[0] += 80
                    case 'brick':
                        if tile_id in range(1, 10):
                            decor_pos[1] += 64
                            decor_pos[0] += 80
                        elif tile_id in range(10, 14):
                            decor_pos[1] += 64
                            decor_pos[0] += 128
                
                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                if self.decor_type != 'brick':
                    tile_offset_x, tile_offset_y = self.getTilePosition(tuple(decor_pos), tile_id, 4)
                else:
                    if tile_id in range(1, 10):
                        tile_offset_x, tile_offset_y = self.getTilePosition(tuple(decor_pos), tile_id, 3)
                    elif tile_id in range(10, 14):
                        tile_offset_x, tile_offset_y = self.getTilePosition(tuple(decor_pos), tile_id, 2)

                decor = Terrain(pos_x, pos_y, self.tile_size, tile_offset_x, tile_offset_y)
                
                self.platform_list.add(decor)

        # Añade los semisolidos a la escena
        for row in range(len(self.scene_semisolid)):
            for col in range(len(self.scene_semisolid[row])):
                tile_id = self.scene_semisolid[row][col]
                if tile_id == 0:
                    continue
                
                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                tile_offset_x, tile_offset_y = self.getTilePosition(self.semisolid_pos, tile_id, 3)

                semisolid = Terrain(pos_x, pos_y, self.tile_size, tile_offset_x, tile_offset_y)
                
                self.semisolid_list.add(semisolid)

        # Añade los coleccionables a la escena
        for row in range(len(self.scene_collectables)):
            for col in range(len(self.scene_collectables[row])):
                tile_id = self.scene_collectables[row][col]
                if tile_id == 0:
                    continue
                
                fruit = Fruits(self.fruit_palette[tile_id])
                
                fruit.rect.x = (col * self.tile_size) - (fruit.rect.width//4)
                fruit.rect.y = (row * self.tile_size) - (fruit.rect.height//4)

                self.collectables_list.add(fruit)
                self.all_sprites.add(fruit)
        
        # Añade los enemigos a la escena
        for row in range(len(self.scene_enemies)):
            for col in range(len(self.scene_enemies[row])):
                tile_id = self.scene_enemies[row][col]
                if tile_id == 0:
                    continue

                enemy = None

                match tile_id:
                    case 1:
                        enemy = Trunk(screenW, screenH)
                    case 2:
                        enemy = Plant(screenW, screenH)
                    case 3:
                        enemy = Mushroom(screenW, screenH)
                    case 4:
                        enemy = BlueBird(screenW, screenH)
                    case 5:
                        enemy = Slime(screenW, screenH)
                    case 6:
                        enemy = Radish(screenW, screenH)

                pos_x = col * self.tile_size
                pos_y = row * self.tile_size

                if pos_x < (screenW // 2) - self.tile_size:
                    enemy.moveSpeed = abs(enemy.moveSpeed)
                else:
                    enemy.moveSpeed = -abs(enemy.moveSpeed)
                
                enemy.rect.x = pos_x
                enemy.rect.y = pos_y - (enemy.rect.height // 2)

                if tile_id == 5:
                    enemy.rect.y += 2

                self.enemy_list.add(enemy)
                self.all_sprites.add(enemy)
        
    def getCollectables(self):
        """ Devuelve la lista de coleccionables.
        """
        return self.collectables_list
    
    def getPlatforms(self):
        """ Devuelve la lista de plataformas.
        """
        return self.platform_list
    
    def getSemisolids(self):
        """ Devuelve la lista de semisolidos.
        """
        return self.semisolid_list
    
    def getEnemies(self):
        """ Devuelve la lista de enemigos.
        """
        return self.enemy_list
    
    def getSprites(self):
        """ Devuelve la lista de todos los sprites.
        """
        return self.all_sprites
    
    def getEndPoint(self):
        """ Devuelve el punto final de la escena, si existe.
        """
        return self.endpoint if self.endpoint else (0, 0)
    
    def getTilePosition(self, pos: tuple, tile_id, size):
        """ Obtiene la posicion del sprite del terreno.
        """
        if size == 2:
            tile_offset_x = pos[0] + self.tile_mult * ((tile_id - 10) % size)
            tile_offset_y = pos[1] + self.tile_mult * ((tile_id - 10) // size)
        else:
            tile_offset_x = pos[0] + self.tile_mult * ((tile_id - 1) % size)
            tile_offset_y = pos[1] + self.tile_mult * ((tile_id - 1) // size)

        return tile_offset_x, tile_offset_y

    def draw(self, screen):
        """ Dibuja los sprites en la escena.
        """
        screen.fill((0, 0, 0))
        for tile in self.tiles:
            screen.blit(self.background, tile)
        self.platform_list.draw(screen)
        self.semisolid_list.draw(screen)
        self.all_sprites.draw(screen)
    
    def update(self):
        """ Actualiza todos los sprites de la escena.
        """
        self.all_sprites.update()

    def clear(self):
        """ Borra todos los elementos de la escena.
        """
        self.tiles.clear()
        self.platform_list.empty()
        self.semisolid_list.empty()
        self.collectables_list.empty()
        self.all_sprites.empty()