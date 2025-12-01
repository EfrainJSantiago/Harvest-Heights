import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Valores por default del sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Guarda el tamaño del sprite
        self.width = width
        self.height = height

    def draw(self, screen):
        """ Dibuja el sprite a la pantalla.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))