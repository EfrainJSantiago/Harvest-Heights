import pygame

class NPC_IDLE(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH, character, direction = 'right'):
        super().__init__()
        # importar imagen de saltar, caer y idle
        path = "assets/Main Characters/" + character + '/Idle (32x32).png'
        
        self.animation = {}
        self.animation_speed = 3
        self.tick = 0
        self.mask = None

        # Load Player Sprites
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction == 'left':
            flipped_sprites = sprites[:]
            for i in range(len(flipped_sprites)):
                flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
            self.animation["Idle"] = flipped_sprites
        else:
            self.animation["Idle"] = sprites

        self.image = self.animation["Idle"][0]
        self.screenW = screenW
        self.screenH = screenH
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # Other
        self.level = None
        self.facingLeft = False
        self.done = False
        self.spawn_pos = None
        self.hurt = False

    def update(self):
        """ Anima al NPC. """

        sprites = self.animation["Idle"]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)