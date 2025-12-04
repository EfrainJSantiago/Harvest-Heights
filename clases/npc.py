import pygame

class NPC_IDLE(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH, character, direction = 'right'):
        super().__init__()
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Importar imagen de idle
        path = "assets/Main Characters/" + character + '/Idle (32x32).png'

        # Carga los sprite sheet de idle
        self.animation = {}
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sprites = []

        # Por cada sprite en el sprite sheet, crea una instancia del sprite
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        # Si la dirección especificada es izquierda,
        # guarda todos los sprites en su direccion opuesta.
        if direction == 'left':
            flipped_sprites = sprites[:]
            for i in range(len(flipped_sprites)):
                flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
            self.animation["Idle"] = flipped_sprites
        # De lo contrario, guarda todos los sprites en su direccion default.
        else:
            self.animation["Idle"] = sprites

        # Prepara la animación de idle
        self.image = self.animation["Idle"][0]
        self.rect = self.image.get_rect()

        # Variables de animación
        self.animation_speed = 3
        self.tick = 0
        self.done = False

    def update(self):
        """ Anima al NPC.
        """
        # Actualiza el sprite del enemigo para la animarlo.
        sprites = self.animation["Idle"]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1