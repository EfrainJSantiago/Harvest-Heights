import pygame
# from clases.object import Object

class Fruits(pygame.sprite.Sprite):
    def __init__(self, fruit):
        super().__init__()
        sprite_sheet = pygame.image.load("assets/Items/Fruits/" + fruit + ".png").convert_alpha()
        self.animation = []
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            self.animation.append(pygame.transform.scale2x(surface))
        
        sprite_sheet = pygame.image.load("assets/Items/Fruits/Collected.png").convert_alpha()
        self.collect_animation = []
        for i in range(sprite_sheet.get_width() // 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            self.collect_animation.append(pygame.transform.scale2x(surface))
        
        self.image = self.animation[0]
        self.animation_speed = 3
        self.tick = 0
        self.mask = None
        self.rect = self.image.get_rect()
        self.collected = False
        self.done = False
    
    def update(self):
        if self.done:
            self.kill()
        elif not self.collected:
            sprite_index = (self.tick // self.animation_speed) % len(self.animation)
            self.image = self.animation[sprite_index]
            self.tick += 1
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)
        elif self.collected:
            sprite_index = (self.tick // self.animation_speed) % len(self.collect_animation)
            self.image = self.collect_animation[sprite_index]
            self.tick += 1
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)
            if sprite_index == len(self.collect_animation) - 1:
                self.done = True