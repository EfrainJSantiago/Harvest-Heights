import pygame
from clases.scene import Scene
from clases.checkpoint import Checkpoint

class Level:
    def __init__(self, screen, player, scenes, level_music):
        # Listas de sprites
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.semisolid_list = pygame.sprite.Group()
        self.collectables_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()

        # Guarda la dirección de la musica del nivel
        self.level_music = level_music

        # Variables de la escena
        self.scene_values = scenes
        self.scenes = []
        self.current_scene_num = 0
        self.current_scene = None
        self.num_scenes = len(scenes)
        self.respawn_point = None
        self.end_point = None
        self.end_goal = None

        # Otras variables
        self.screen = screen
        self.player = player

    def startGame(self, screenW, screenH):
        """ Crea un nuevo nivel del juego.
        """
        for scene in self.scene_values:
            self.scenes.append(Scene(scene))
        self.current_scene_num = 0
        self.load_scene(screenW, screenH)

        self.all_sprites.add(self.player)

        if self.level_music != '':
            pygame.mixer.music.load(self.level_music)
            pygame.mixer.music.set_volume(0.5)
    
    def load_music(self):
        """ Carga la musica del nivel.
        """
        if self.level_music != '':
            pygame.mixer.music.load(self.level_music)
            pygame.mixer.music.set_volume(0.5)

    def play_music(self):
        """ Reproduce la musica del nivel.
        """
        if self.level_music != '':
            pygame.mixer.music.play(-1)
    
    def pause_music(self):
        """ Pausa la musica del nivel.
        """
        if self.level_music != '':
            pygame.mixer.music.pause()

    def unpause_music(self):
        """ Resume la musica del nivel.
        """
        if self.level_music != '':
            pygame.mixer.music.unload()
    
    def stop_music(self):
        """ Detiene la musica del nivel.
        """
        if self.level_music != '':
            pygame.mixer.music.stop()

    def restartLevel(self):
        """ Reinicia el nivel.
        """
        self.current_scene.clear()
        self.clear()
    
    def resetScene(self, screenW, screenH):
        """ Reinicia la escena.
        """
        self.player.disappear = False
        if self.end_goal:
            self.end_goal.kill()
            self.end_goal = None
        self.current_scene.clear()
        self.load_scene(screenW, screenH)

    def progress(self, screenW, screenH):
        """ Borra la escena actual y carga la proxima escena.
        """
        self.current_scene.clear()
        self.current_scene_num += 1
        self.load_scene(screenW, screenH)
    
    def load_scene(self, screenW, screenH):
        """ Carga la escena.
        """
        # Obtiene la escena actual
        self.current_scene = self.scenes[self.current_scene_num]
        self.current_scene.constructScene(screenW, screenH)
        self.respawn_point = self.current_scene.respawn_point

        # Inicializa la posición y estado del jugador
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1] - self.player.rect.height
        self.player.falling = True
        self.player.change_y = 0

        # Obtiene todos los sprites en la escena
        self.platform_list = self.current_scene.getPlatforms()
        self.collectables_list = self.current_scene.getCollectables()
        self.all_sprites = self.current_scene.getSprites()
        self.semisolid_list = self.current_scene.getSemisolids()
        self.enemy_list = self.current_scene.getEnemies()

        # Asigna el nivel actual a la variable nivel de todos los enemigos.
        for enemy in self.enemy_list:
            enemy.level = self
        
        self.all_sprites.add(self.player)

    def update(self):
        """ Actualiza todos los sprites de la escena.
        """
        self.current_scene.update()
        if self.end_goal:
            self.end_goal.update()

    def draw(self, screen):
        """ Dibuja todos los sprites en la pantalla.
        """
        screen.fill((0, 0, 0))
        self.current_scene.draw(screen)
        self.all_sprites.draw(screen)
    
    def checkComplete(self):
        """ Verifica si la escena ha sido completada.
        """
        # Si no es la ultima escena.
        if self.current_scene_num != self.num_scenes - 1:
            # Si no quedan collecionables por colleccionar, 
            # la escena ha sido completada
            if len(self.collectables_list) == 0:
                return True
            # De lo contrario, si queda solo 1, verifica si ha sido coleccionada
            elif len(self.collectables_list) == 1:
                for collectable in self.collectables_list:
                    # Si el coleccionable ha sido coleccionado, desaparece al jugador
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
            # Si el punto final esta activo
            if self.end_goal:
                # Si la animación del punto final ha sido activada,
                # la escena ha sido completada
                if self.end_goal.goal and not self.end_goal.animate:
                    return True
                # De lo contrario, si el jugador no ha desaparecido,
                # hazlo desaparecer
                elif self.end_goal.goal and not self.player.disappear:
                    self.player.disappear = True
                    self.player.tick = 0
                    self.player.image_key = "Desappearing"
                    self.player.update()
                    return False
            # Si no quedan coleccionables en la escena, activa el punto final
            elif len(self.collectables_list) == 0:
                self.end_point = self.current_scene.getEndPoint()
                self.end_goal = Checkpoint("End")
                self.end_goal.rect.x = self.end_point[0] - self.end_goal.rect.width
                self.end_goal.rect.y = self.end_point[1] - self.end_goal.rect.height
                self.all_sprites.add(self.end_goal)
                return False
            return False

    def checkFinished(self):
        """ Verifica si el nivel ha sido completado.
        """
        if self.end_goal and self.end_goal.goal and not self.end_goal.animate:
            return True
        else:
            return False

    def collect(self):
        """ Verifica si el jugador ha colleccionado algun colleccionable.
        """
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
        """ Borra todos los elementos del nivel.
        """
        self.scenes.clear()
        self.semisolid_list.empty()
        self.collectables_list.empty()
        self.enemy_list.empty()
        self.platform_list.empty()
        self.all_sprites.empty()