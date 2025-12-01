import pygame
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
        self.projectile_list = pygame.sprite.Group()
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

    def startGame(self, screen, screenW, screenH):
        for scene in self.scene_values:
            self.scenes.append(Scene(scene))
        self.current_scene_num = 0
        self.load_scene(screen, screenW, screenH)

        self.all_sprites.add(self.player)

    def restartLevel(self):
        self.current_scene.clear()
        self.clear()
    
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

    def update(self):
        self.current_scene.update()
        if self.end_goal:
            self.end_goal.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
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
                if pygame.sprite.collide_mask(self.player, sprite) and not sprite.collected:
                    sprite.collected = True
                    sprite.tick = 0
                    
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
    
    # No eliminar por si se decide usar para detectar si el jugador choco con algun enemigo
    # Pero hasta el momento, puede que los mismos enemigos lo detecten
    # def collide_big_enemy(self, big_enemy):
    #     if big_enemy.colliderect(self.player.rect):
    #         return True
    #     return False