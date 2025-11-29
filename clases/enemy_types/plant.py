import pygame
from clases.enemy import Enemy

class Plant(Enemy):
    def __init__(self, screenW, screenH):
        super().__init__("Plant")
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Asigna un sprite por default
        self.image = self.all_sprites["Idle_left"][0]
        self.image_key = "Idle"
        self.rect = self.image.get_rect()
        self.moveSpeed = 0

        self.fire_delay = 60
        self.fire_tick = 0
        self.attack = False
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        self.fire_tick += 1

        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de ataque, regresa a Idle
            if self.attack:
                self.idle = True
                self.attack = False
                self.image_key = "Idle"
                self.tick = 0
                self.done = False

        super().update()

        # Asegura de que el enemigo aparezca al tope del bloque si esta desplazado
        block_hit_list = (pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False))

        for block in block_hit_list:
            # Reinicia su posición en base al tope/fondo del objeto
            if self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
        
        rect_left = 0
        width = 0
        if self.facingRight:
            rect_left = self.screenW
        if rect_left > 0:
            width = (rect_left - self.rect.centerx)
        else:
            width = self.screenW - (self.screenW - self.rect.centerx)
        rect = pygame.Rect(rect_left, self.rect.centery, width, 2)

        if rect.colliderect(self.level.player.rect) and self.fire_tick >= self.fire_delay:
            print('Yo')
            self.done = False
            self.idle = False
            self.fire_tick = 0
            self.attack = True
            self.image_key = "Attack"
            self.tick = 0