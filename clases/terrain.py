import pygame
from clases.object import Object

class Terrain(Object):
    def __init__(self, x, y, size, x_pos, y_pos):
        super().__init__(x, y, size, size)

        # Importar la imagen a ser usada
        image = pygame.image.load("assets/Terrain/Terrain (16x16).png").convert_alpha()

        # Crea una instancia del sprite, teniendo en cuenta el tamaño
        # y posición del sprite deseado.
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(x_pos, y_pos, size, size)
        surface.blit(image, (0, 0), rect)
        self.terrain = pygame.transform.scale2x(surface)
        self.image.blit(self.terrain, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)