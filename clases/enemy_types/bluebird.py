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
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_box = pygame.Rect(0, 0, 60, 44)

        # Variables de movimiento
        self.moveSpeed = 2
    
    def move(self):
        """ Mueve al enemigo horizontalmente
        """
        if self.hurt:
            return
        
        # Si el enemigo no esta idle, muevelo
        if not self.idle:
            self.rect.x += self.moveSpeed
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        self.hit_box.center = self.rect.center
        
        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de idle, vuelve a correr
            if self.idle:
                self.idle = False
                self.tick = 0
                self.done = False
                self.turnLock = False
            
            # Si es la de golpe, matalo
            if self.hurt:
                self.kill()

        self.move()
        super().update()

        if self.hurt:
            return

        # Asegura de que el enemigo aparezca al alineado a los bloques si esta desplazado
        block_hit_list = (pygame.sprite.spritecollide(self, self.level.platform_list, False))

        for block in block_hit_list:
            if self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
            elif self.rect.top <= block.rect.bottom:
                self.rect.top = block.rect.bottom
            elif self.rect.right >= block.rect.left:
                self.rect.right = block.rect.left
            elif self.rect.left <= block.rect.right:
                self.rect.left = block.rect.right

        # Explora frente a si mismo para evitar chocar
        probe = self.rect.copy()
        if self.moveSpeed > 0:
            probe.x += (self.rect.width // 2)
        else:
            probe.x -= (self.rect.width // 2)
        
        platform_hit = False

        for platform in self.level.platform_list:
            if probe.colliderect(platform.rect):
                platform_hit = True
                break

        # Si choco, gira al enemigo
        if platform_hit:
            self.turn()
        
        if probe.right >= self.screenW:
            self.turn()
        elif probe.left < 0:
            self.turn()
        
        # Verifica si el jugador toco al enemigo
        player = self.level.player
        prev_bottom = player.rect.bottom + player.change_y

        if player.hit_box.colliderect(self.hit_box):
            # Si brinco encima, rebota al jugador y golpea al enemigo
            if player.change_y < 0 and player.rect.bottom >= self.hit_box.top and prev_bottom <= self.hit_box.top:
                player.change_y = player.jumpSpeed
                player.jump(False)
                self.hit()
            else:
                if not self.level.player.hurt:
                    self.level.player.hit()
    
    def turn(self):
        """ Gira al enemigo
        """
        if not self.turnLock:
            self.turnLock = True
            self.done = False
            self.moveSpeed *= -1
            self.idle = True
            self.tick = 0
    
    def hit(self):
        """ Lastima al enemigo
        """
        self.hurt = True
        self.image_key = "Hit"
        self.turnLock = True
        self.idle = False
        self.tick = 0
        self.done = False
        self.hit_sound.play()