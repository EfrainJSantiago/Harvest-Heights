import pygame
#from clases.enemy import Enemy
#from clases.platform import Platform
from clases.terrain import Terrain
import random

class Level:
    def __init__(self, screen, player, background):
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = player
        self.terrain = pygame.image.load("assets/Terrain/Terrain (16x16).png").convert()
        self.background = pygame.image.load("assets/Background/" + background + ".png").convert()
        _, _, width, height = self.background.get_rect()
        self.tiles = []

        for i in range(screen.width // width + 1):
            for j in range(screen.height // height + 1):
                pos = (i * width, j * width)
                self.tiles.append(pos)
        
        floor_pos = 96
        self.floor = [Terrain(i * 32, screen.height - 32, 32, floor_pos + 16) for i in range(-screen.width // 32, (screen.width * 2) // 32)]
        self.floor[0] = Terrain(0, screen.height - 32, 32, floor_pos)
        #self.floor[-2] = Terrain(0, screen.height - 32, 32, floor_pos + 32)

        # 19 tile width, 13 tile height

    def startGame(self, width, height):
        self.player.rect.x = 0
        self.player.rect.y = height - self.player.rect.height - self.floor[0].rect.height
        for floor_obj in self.floor:
            self.platform_list.add(floor_obj)
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
        for tile in self.tiles:
            screen.blit(self.background, tile)
        for obj in self.floor:
            obj.draw(screen)
    #     self.enemy_list.draw(screen)
    #     self.platform_list.draw(screen)
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