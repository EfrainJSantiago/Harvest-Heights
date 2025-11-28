import pygame
#from clases.enemy import Enemy
#from clases.platform import Platform
from clases.terrain import Terrain
from clases.scene import Scene
from clases.player import Player
from clases.checkpoint import Checkpoint
import random

class Level:
    def __init__(self, screen, player, scenes):
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.semisolid_list = pygame.sprite.Group()
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
        self.end_goal = None

        for scene in scenes:
            self.scenes.append(Scene(scene))

        # 19 tile width, 13 tile height

    def startGame(self, screen, width, height):
        self.load_scene(screen)
        # self.current_scene = self.scenes[0]
        # self.current_scene.constructScene(screen)
        # self.respawn_point = self.current_scene.respawn_point
        # self.player.rect.x = self.respawn_point[0]
        # self.player.rect.y = self.respawn_point[1] - self.player.rect.height
        # self.player.falling = True
        # self.player.change_y = 0
        # self.platform_list = self.current_scene.getPlatforms()
        # # for platform in self.platform_list:
        # #     self.all_sprites.add(platform)
        # self.collectables_list = self.current_scene.getCollectables()
        # # for collectable in self.collectables_list:
        # #     self.all_sprites.add(collectable)
        # self.all_sprites = self.current_scene.getSprites()
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
    def progress(self, screen):
        self.current_scene.clear()
        self.current_scene_num += 1
        self.load_scene(screen)
    
    def load_scene(self, screen):
        self.current_scene = self.scenes[self.current_scene_num]
        self.current_scene.constructScene(screen)
        self.respawn_point = self.current_scene.respawn_point
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1] - self.player.rect.height
        self.player.falling = True
        self.player.change_y = 0
        self.platform_list = self.current_scene.getPlatforms()
        self.collectables_list = self.current_scene.getCollectables()
        self.all_sprites = self.current_scene.getSprites()
        self.semisolid_list = self.current_scene.getSemisolids()
        self.all_sprites.add(self.player)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.current_scene.update()
        if self.end_goal:
            self.end_goal.update()
    #     self.enemy_list.draw(screen)
        self.current_scene.draw(screen)
        self.all_sprites.draw(screen)
    
    def checkComplete(self):
        if self.current_scene_num != len(self.scenes) - 1:
            if len(self.collectables_list) == 0:
                return True
            elif len(self.collectables_list) == 1:
                for collectable in self.collectables_list:
                    if collectable.collected and not self.player.disappear:
                        self.player.disappear = True
                        self.player.tick = 0
                        self.player.image_key = "Desappearing"
                        self.player.update()
                        return False
            else:
                return False
        else:
            if self.end_goal:
                if self.end_goal.goal and not self.end_goal.animate:
                    return True
                elif self.end_goal.goal and not self.player.disappear:
                    self.player.disappear = True
                    self.player.tick = 0
                    self.player.image_key = "Desappearing"
                    self.player.update()
                    return False
            elif len(self.collectables_list) == 0:
                self.end_point = self.current_scene.getEndPoint()
                self.end_goal = Checkpoint("End")
                self.end_goal.rect.x = self.end_point[0] - self.end_goal.rect.width
                self.end_goal.rect.y = self.end_point[1] - self.end_goal.rect.height
                #self.platform_list.add(self.end_goal)
                self.all_sprites.add(self.end_goal)
                return False
            return False

    def checkFinished(self):
        if self.end_goal and self.end_goal.goal and not self.end_goal.animate:
            return True
        else:
            return False

    def collect(self):
        if not self.player.appear:
            sprite_hit = pygame.sprite.spritecollide(self.player, self.collectables_list, False)
            for sprite in sprite_hit:
                if not sprite.collected:
                    sprite.collected = True
                    sprite.tick = 0
    #     point = 0
    #     if sprite_hit:
    #         point = point + 1
    #     return point

    def respawn_player(self, player):
        """ Respawns player if player was killed
        """
        self.player = player
        self.all_sprites.add(self.player)

    # def collide_big_enemy(self, big_enemy):
    #     if big_enemy.colliderect(self.player.rect):
    #         return True
    #     return False