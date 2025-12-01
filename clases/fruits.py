import pygame
# from clases.object import Object

class Fruits(pygame.sprite.Sprite):
    def __init__(self, fruit):
        super().__init__()
        
        # Carga el sprite sheet de la fruta
        sprite_sheet = pygame.image.load("assets/Items/Fruits/" + fruit + ".png").convert_alpha()
        self.animation = []

        # Por cada sprite en el sprite sheet, crea una instancia del sprite
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            self.animation.append(pygame.transform.scale2x(surface))
        
        # Carga el sprite sheet de collección
        sprite_sheet = pygame.image.load("assets/Items/Fruits/Collected.png").convert_alpha()
        self.collect_animation = []
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            self.collect_animation.append(pygame.transform.scale2x(surface))
        
        # Prepara la animación de la fruta
        self.image = self.animation[0]

        # Variables para calcular toque
        self.rect = self.image.get_rect()
        self.mask = None

        # Variables de animación
        self.animation_speed = 3
        self.tick = 0
        self.done = False

        # Variables de estado
        self.collected = False
        self.sound_played = False

        # Variables de sonido
        self.collect_sound = pygame.mixer.Sound("sounds/Retro PickUp 18.wav")
        self.collect_sound.set_volume(0.1)
    
    def update(self):
        """ Actualiza el estado de la fruta.
        """
        # Si termino la animación de colección
        if self.done:
            self.kill()

        # Si no ha sido coleccionado, haz la animación de costumbre
        if not self.collected:
            sprite_index = (self.tick // self.animation_speed) % len(self.animation)
            self.image = self.animation[sprite_index]
            self.tick += 1
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

        # Si ha sido coleccionado, haz la animación de colección
        elif self.collected:
            if not self.sound_played:
                self.collect_sound.play()
                self.sound_played = True
            sprite_index = (self.tick // self.animation_speed) % len(self.collect_animation)
            self.image = self.collect_animation[sprite_index]
            self.tick += 1
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)
            if sprite_index == len(self.collect_animation) - 1:
                self.done = True