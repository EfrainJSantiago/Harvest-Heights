import pygame
from clases.enemy import Enemy

class Mushroom(Enemy):
    def __init__(self, screenW, screenH):
        super().__init__("Mushroom")
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Asigna un sprite por default
        self.image = self.all_sprites["Idle_left"][0]
        self.image_key = "Idle"
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
        if self.hurt:
            return
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
        if self.hurt:
            self.rect.y -= self.change_y    # subir/bajar 
            self.change_y -= self.gravity
        
        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de idle, vuelve a correr
            if self.idle:
                self.idle = False
                self.image_key = "Run"
                self.tick = 0
                self.done = False
                self.turnLock = False
            if self.hurt: # Si es la de golpe, matalo
                if self.rect.bottom >= self.screenH + self.rect.width:
                    print('I AM DEAD! NOT BIG SURPRISE.')
                    self.kill()
            if self.hit_wall:
                self.hit_wall = False
                self.facingRight = not self.facingRight
                self.tick = 0

        # Mueve al enemigo
        self.move()
        super().update()
        
        if self.hurt:
            return

        # Verifica si choco algo
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Si se esta moviendo a la derecha,
            # asigna su derecha a la izquierda del objeto que choco.
            if self.moveSpeed > 0:
                self.rect.right = block.rect.left
                self.turn()
            elif self.moveSpeed < 0:
                # De lo contrario, si se esta moviendo a la izquierda, haz lo opuesto.
                self.rect.left = block.rect.right
                self.turn()
        
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

        probe = self.rect.copy()
        if self.moveSpeed > 0:  # Moving right
            probe.x += self.rect.width
        else:                  # Moving left
            probe.x -= self.rect.width
        
        # Verifica si se bajó de una plataforma
        probe.y += 2
        platform_hit = False

        for platform in self.level.platform_list:
            if probe.colliderect(platform.rect):
                platform_hit = True
                break

        if not platform_hit:
            for platform in self.level.semisolid_list:
                if probe.colliderect(platform.rect):
                    platform_hit = True
                    break

        # Si no encuentra una plataforma, gira al enemigo
        if not platform_hit:
            self.turn()
        
        # Si el enemigo llega al vacio al fondo de la pantalla, cuentalo como golpe
        if self.rect.bottom >= self.screenH and not self.hurt:
            self.done = False
            self.falling = False
            self.change_y = 0
            self.hurt = True
            self.image_key = "Hit"
            self.tick = 0
        
        if self.rect.right >= self.screenW:
            self.rect.right = self.screenW
            self.turn()
        elif self.rect.left < 0:
            # De lo contrario, si se esta moviendo a la izquierda, haz lo opuesto.
            self.rect.left = 0
            self.turn()
        
        # Check and see if the player lands on the enemy
        player = self.level.player
        prev_bottom = player.rect.bottom + player.change_y

        if player.rect.colliderect(self.rect):
            if player.change_y < 0 and player.rect.bottom >= self.rect.top and prev_bottom <= self.rect.top:
                player.change_y = (player.jumpSpeed // 2)
                player.jump(False)
                self.done = False
                self.hurt = True
                self.change_y = 4
                self.image_key = "Hit"
                self.tick = 0
    
    def turn(self):
        if not self.turnLock:
            self.turnLock = True
            self.done = False
            self.moveSpeed *= -1
            self.hit_wall = True
            self.idle = True
            self.image_key = "Idle"
            self.tick = 0