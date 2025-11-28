import pygame
from clases.enemy import Enemy

class Trunk(Enemy):
    def __init__(self, screenW, screenH):
        super().__init__("Trunk")
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Valores de movimiento
        self.gravity = 1
        self.moveSpeed = 2
        self.falling = False
        self.change_y = 0
    
    def move(self):
        """ Mueve al enemigo horizontalmente
        """
        # Si el enemigo no esta quieto, muevelo
        if not self.idle:
            self.rect.x -= self.moveSpeed    # Mover el enemigo horizontalmente
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        # Mueve al enemigo
        self.move()

        # Verifica si choco algo
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Si se esta moviendo a la derecha,
            # asigna su derecha a la izquierda del objeto que choco.
            if self.moveSpeed > 0:
                self.rect.right = block.rect.left
                self.moveSpeed *= -1
            elif self.moveSpeed < 0:
                # De lo contrario, si se esta moviendo a la izquierda, haz lo opuesto.
                self.rect.left = block.rect.right
                self.moveSpeed *= -1
        
        # Movimiendo de arriba/abajo
        if self.falling:
            self.rect.y -= self.change_y    # subir/bajar 
            self.change_y -= self.gravity         # gravedad (que tan pesado es el salto/la caida)
            # if self.change_y < 0:
            #     self.falling = True
        
        # Verifica si choco algo
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reinicia su posición en base al tope/fondo del objeto
            if self.change_y < 0:
                self.rect.bottom = block.rect.top
                self.falling = False
                self.change_y = 0
            elif self.change_y > 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0
        
        # Verifica si chocamos un semisolido
        prev_bottom = self.rect.bottom + self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        for block in block_hit_list:

            # Reinicia su posición en base al tope del semisolido
            if self.change_y < 0 and self.rect.bottom >= block.rect.top and prev_bottom <= block.rect.top:
                self.rect.bottom = block.rect.top
                self.falling = False
                self.change_y = 0
        
        # Verifica si se bajó de una plataforma
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        self.rect.y -= 2

        # Si no encuentra una plataforma, baja al enemigo
        if len(platform_hit_list) == 0:
            if not self.falling:
                self.change_y = 0
            self.falling = True
        
        # Si el enemigo llega al vacio al fondo de la pantalla, cuentalo como golpe
        if self.rect.bottom >= self.screenH and not self.hurt:
            self.falling = False
            self.change_y = 0
            self.hurt = True
            self.image_key = "Hit"
            self.tick = 0