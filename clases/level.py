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
        self.scene_values = scenes
        self.player = player
        self.scenes = []
        self.current_scene_num = 0
        self.current_scene = None
        self.num_scenes = len(scenes)
        self.respawn_point = None
        self.end_point = None
        self.start_point = None
        self.end_goal = None
        self.screen = screen

        # 19 tile width, 13 tile height

    def startGame(self, screen, screenW, screenH):
        for scene in self.scene_values:
            self.scenes.append(Scene(scene))
        self.current_scene_num = 0
        self.load_scene(screen, screenW, screenH)
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

    def restartLevel(self, screen, width, height):
        self.player.disappear = False
        self.current_scene.clear()
        self.clear()
        self.startGame(screen, width, height)
    
    def resetScene(self, screen, screenW, screenH):
        self.player.disappear = False
        if self.end_goal:
            self.end_goal.kill()
            self.end_goal = None
        self.current_scene.clear()
        self.load_scene(screen, screenW, screenH)

    def progress(self, screen, screenW, screenH):
        self.current_scene.clear()
        self.current_scene_num += 1
        self.load_scene(screen, screenW, screenH)
    
    def load_scene(self, screen, screenW, screenH):
        self.current_scene = self.scenes[self.current_scene_num]
        self.current_scene.constructScene(screen, screenW, screenH)
        self.respawn_point = self.current_scene.respawn_point
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1] - self.player.rect.height
        self.player.falling = True
        self.player.change_y = 0
        self.platform_list = self.current_scene.getPlatforms()
        self.collectables_list = self.current_scene.getCollectables()
        self.all_sprites = self.current_scene.getSprites()
        self.semisolid_list = self.current_scene.getSemisolids()
        self.enemy_list = self.current_scene.getEnemies()
        for enemy in self.enemy_list:
            enemy.level = self
        self.all_sprites.add(self.player)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.current_scene.update()
        if self.end_goal:
            self.end_goal.update()
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
    
    def clear(self):
        self.scenes.clear()
        self.semisolid_list.empty()
        self.collectables_list.empty()
        self.enemy_list.empty()
        self.platform_list.empty()
        self.all_sprites.empty()

    # def collide_big_enemy(self, big_enemy):
    #     if big_enemy.colliderect(self.player.rect):
    #         return True
    #     return False