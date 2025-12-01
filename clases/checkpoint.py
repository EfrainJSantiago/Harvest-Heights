import pygame
# from clases.object import Object

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        path = "assets/Items/Checkpoints/"
        self.images = []
        if type == 'Start' or type == 'End':
            self.images = [type + " (Idle).png"]
            if type == 'End':
                self.images.append(type + " (Pressed) (64x64).png")
            else:
                self.images.append(type + " (Moving) (64x64).png")
        else:
            self.images = ["Checkpoing (Flag Idle)(64x64).png",
                      "Checkpoing (Flag Out)(64x64).png",
                      "Checkpoing (No Flag).png"]
        
        self.all_sprites = {}
        self.triggered = pygame.mixer.Sound("sounds/Retro Success Melody 02 - choir soprano.wav")
        self.triggered.set_volume(0.3)
            
        # Load Checkpoint Sprites
        for image in self.images:
            sprite_sheet = pygame.image.load(path + type + '/' + image).convert_alpha()
            sprites = []
            for i in range(sprite_sheet.get_width() // 64):
                surface = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * 64, 0, 64, 64)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            
            self.all_sprites[image] = sprites
        
        self.image_key = None
        if type == 'Checkpoint':
            self.image_key = self.images[2]
        else:
            self.image_key = self.images[0]
        self.image = self.all_sprites[self.image_key][0]
        self.animation_speed = 3
        self.tick = 0
        self.mask = None
        self.rect = self.image.get_rect()
        self.done = False
        self.animate = False
        self.goal = False
    
    def update(self):
        if self.done:
            self.image_key = self.images[0]
            self.animate = False
            self.done = False
        
        sprites = self.all_sprites[self.image_key]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animate and sprite_index == len(sprites) - 1:
            self.done = True
    
    def trigger(self):
        if not self.animate:
            self.triggered.play()
            self.animate = True
            self.image_key = self.images[1]
            self.tick = 0
            self.goal = True