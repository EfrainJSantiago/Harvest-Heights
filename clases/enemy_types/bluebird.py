import pygame
from clases.enemy import Enemy

class BlueBird(Enemy):
    def __init__(self, screenW, screenH):
        super().__init__("BlueBird")
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Asigna un sprite por default
        self.image = self.all_sprites["Flying_left"][0]
        self.image_key = "Flying"
        self.rect = self.image.get_rect()

        # Valores de movimiento
        self.gravity = 1
        self.falling = False
        self.change_y = 0
        self.hit_wall = False
        self.moveSpeed = 2
    
    def move(self):
        """ Mueve al enemigo horizontalmente
        """
        # Si el enemigo no esta quieto, muevelo
        if not self.idle:
            self.rect.x += self.moveSpeed    # Mover el enemigo horizontalmente
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        # Gira al enemigo
        # if self.hit_wall and not self.idle:
        #     self.hit_wall = False
        #     self.facingRight = not self.facingRight
        #     self.tick = 0
        
        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de idle, vuelve a correr
            if self.idle:
                self.idle = False
                self.tick = 0
                self.done = False
                self.turnLock = False
            if self.hurt: # Si es la de golpe, matalo
                self.kill()
            if self.hit_wall:
                self.hit_wall = False
                self.facingRight = not self.facingRight
                self.tick = 0

        # Mueve al enemigo
        self.move()
        super().update()

        # # Verifica si choco algo
        # block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # for block in block_hit_list:
        #     # Si se esta moviendo a la derecha,
        #     # asigna su derecha a la izquierda del objeto que choco.
        #     if self.moveSpeed > 0:
        #         self.rect.right = block.rect.left
        #         self.turn()
        #     elif self.moveSpeed < 0:
        #         # De lo contrario, si se esta moviendo a la izquierda, haz lo opuesto.
        #         self.rect.left = block.rect.right
        #         self.turn()

        probe = self.rect.copy()
        if self.moveSpeed > 0:  # Moving right
            probe.x += (self.rect.width // 2)
        else:                  # Moving left
            probe.x -= (self.rect.width // 2)
        
        # Verifica si se bajó de una plataforma
        probe.y += 2
        platform_hit = False

        for platform in self.level.platform_list:
            if probe.colliderect(platform.rect):
                platform_hit = True
                break

        # Si no encuentra una plataforma, gira al enemigo
        if platform_hit:
            self.turn()
        
        if probe.right >= self.screenW:
            self.turn()
        elif probe.left < 0:
            # De lo contrario, si se esta moviendo a la izquierda, haz lo opuesto.
            self.turn()
    
    def turn(self):
        if not self.turnLock:
            self.turnLock = True
            self.done = False
            self.moveSpeed *= -1
            self.hit_wall = True
            self.idle = True
            self.tick = 0