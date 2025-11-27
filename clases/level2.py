import pygame
#from clases.enemy import Enemy
#from clases.platform import Platform
from clases.terrain import Terrain
from clases.scene import Scene
from clases.player import Player
import random

class Level:
    def __init__(self, screen, player, scenes):
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.collectables_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = player
        self.scenes = []
        self.current_scene_num = 0
        self.current_scene = None
        self.num_scenes = len(scenes)
        self.respawn_point = None
        self.end_point = None
        self.start_point = None

        for scene in scenes:
            self.scenes.append(Scene(scene))

        # 19 tile width, 13 tile height

    def startGame(self, screen, width, height):
        self.current_scene = self.scenes[0]
        self.current_scene.constructScene(screen)
        self.respawn_point = self.current_scene.respawn_point
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1] - self.player.rect.height
        self.player.falling = True
        self.player.change_y = 0
        self.platform_list = self.current_scene.getPlatforms()
        self.collectables_list = self.current_scene.getCollectables()
        self.all_sprites = self.current_scene.getSprites()
    #     # Add all floor
    #     for i in range(5):
    #         block = Enemy((255, 0, 0), 60, 60)

    #         block.rect.x = random.randrange(width)
    #         block.rect.y = random.randrange(height)

    #         self.enemy_list.add(block)
    #         self.all_sprites.add(block)

    #     # Add all level platforms
    #     # Array with width, height, x, and y of platform
    #     level = [[100, 70, 50, 300],
    #              [100, 70, 150, 350],
    #              [100, 70, 100, 200],
    #              ]

    #     # Go through the array above and add platforms
    #     for platform in level:
    #         block = Platform(platform[0], platform[1])
    #         block.rect.x = platform[2]
    #         block.rect.y = platform[3]
    #         block.player = self.player
    #         self.platform_list.add(block)

        self.all_sprites.add(self.player)

    # def restartGame(self, width, height):
    #     self.player.rect.x = 0
    #     self.player.rect.y = 0
    #     self.enemy_list.empty()
    #     self.all_sprites.empty()
    #     self.platform_list.empty()
    #     self.startGame(width, height)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.current_scene.update()
    #     self.enemy_list.draw(screen)
        self.current_scene.draw(screen)
        self.all_sprites.draw(screen)

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