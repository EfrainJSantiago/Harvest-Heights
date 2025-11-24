import pygame
from clases.object import Object

class Terrain(Object):
    def __init__(self, x, y, size, pos):
        super().__init__(x, y, size, size)
        image = pygame.image.load("assets/Terrain/Terrain (16x16).png").convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(pos, 0, size, size)
        surface.blit(image, (0, 0), rect)
        self.terrain = pygame.transform.scale2x(surface)
        self.image.blit(self.terrain, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)