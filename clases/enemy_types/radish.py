import pygame
from clases.enemy import Enemy

class Radish(Enemy):
    def __init__(self, screenW, screenH):
        super().__init__("Radish")
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Asigna un sprite por default
        self.image = self.all_sprites["Idle 1_left"][0]
        self.image_key = "Idle 1"
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_box = pygame.Rect(0, 0, 54, 56)

        # Valores de movimiento
        self.gravity = 1
        self.falling = False
        self.change_y = 0
        self.moveSpeed = 2
        self.health = 2
    
    def move(self):
        """ Mueve al enemigo horizontalmente
        """
        if self.hurt:
            return
        
        # Si el enemigo no esta quieto, muevelo
        if not self.idle and self.health == 1:
            self.rect.x += (self.moveSpeed * 2)    # Mover el enemigo horizontalmente
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        self.hit_box.bottom = self.rect.bottom
        self.hit_box.centerx = self.rect.centerx - 2
        
        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de idle, vuelve a correr
            if self.idle:
                self.idle = False
                self.tick = 0
                self.done = False
                self.turnLock = False
                if self.health == 1:
                    self.image_key = "Run"
            if self.hurt and self.health == 0: # Si es la de golpe, matalo
                self.kill()
            if self.hurt and self.health > 0:
                self.hurt = False
                self.falling = False
                self.tick = 0
                self.image_key = "Run"
                self.turnLock = False

        # Mueve al enemigo
        self.move()
        super().update()

        if self.health == 2:
            # Check and see if the player lands on the enemy
            player = self.level.player
            prev_bottom = player.rect.bottom + player.change_y

            if player.hit_box.colliderect(self.hit_box):
                if player.change_y < 0 and player.rect.bottom >= self.hit_box.top and prev_bottom <= self.hit_box.top:
                    player.change_y = (player.jumpSpeed // 2)
                    player.jump(False)
                    self.hit()
                else:
                    if not self.level.player.hurt:
                        self.level.player.hit()
            return
        
        if self.hurt and self.health == 0:
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
        
        if self.health == 1 and not self.hurt:
            # Check and see if the player lands on the enemy
            player = self.level.player
            prev_bottom = player.rect.bottom + player.change_y

            if player.hit_box.colliderect(self.hit_box):
                if player.change_y < 0 and player.rect.bottom >= self.hit_box.top and prev_bottom <= self.hit_box.top:
                    player.change_y = (player.jumpSpeed // 2)
                    player.jump(False)
                    self.hit()
                else:
                    if not self.level.player.hurt:
                        self.level.player.hit()
    
    def turn(self):
        if not self.turnLock:
            self.turnLock = True
            self.done = False
            self.moveSpeed *= -1
            self.idle = True
            self.tick = 0
            if self.health == 1:
                self.image_key = "Idle 2"
    
    def hit(self):
        self.done = False
        self.hurt = True
        self.falling = True
        self.image_key = "Hit"
        self.tick = 0
        self.health -= 1
        self.turnLock = True
        self.hit_sound.play()