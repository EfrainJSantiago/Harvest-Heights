import pygame
from clases.enemy import Enemy
from clases.projectile import Projectile

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
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_box = pygame.Rect(0, 0, 56, 70)

        # Variables de ataque
        self.fire_delay = 60
        self.fire_tick = 0
        self.attack = False
        self.fire_lock = True

        # Variables de sonido
        self.shot = pygame.mixer.Sound("sounds/Retro Blop 18.wav")
        self.shot.set_volume(0.2)
    
    def update(self):
        """ Actualiza el status del enemigo
        """
        self.hit_box.bottom = self.rect.bottom
        self.hit_box.centerx = self.rect.centerx + 1
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
            
            # Si es la de golpe, matalo
            if self.hurt:
                self.kill()
        else:
            if self.attack and not self.fire_lock:
                sprite_index = (self.tick // self.animation_speed) % 8
                if sprite_index == 5:
                    bullet = None
                    if self.moveSpeed > 0:
                        bullet = Projectile('right', self.level)
                        bullet.rect.left = self.rect.right - (bullet.rect.width // 2)
                    else:
                        bullet = Projectile('left', self.level)
                        bullet.rect.right = self.rect.left + (bullet.rect.width // 2)
                    
                    bullet.rect.centery = self.rect.centery - 5
                    self.level.projectile_list.add(bullet)
                    self.level.all_sprites.add(bullet)
                    self.shot.play()
                    self.fire_lock = True

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
        
        block_hit_list = (pygame.sprite.spritecollide(self, self.level.semisolid_list, False))

        for block in block_hit_list:
            if self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
        
        # Verifica si el jugador esta en su linea de mirada.
        rect_left = 0
        width = 0

        if self.moveSpeed > 0:
            rect_left = self.screenW

        if rect_left > 0:
            width = (rect_left - self.rect.centerx)
        else:
            width = self.screenW - (self.screenW - self.rect.centerx)
        rect = pygame.Rect(rect_left, self.rect.centery, width, 2)

        # Si encuentra al jugador, ataca
        if rect.colliderect(self.level.player.hit_box) and self.fire_tick >= self.fire_delay and not self.level.player.appear:
            self.done = False
            self.idle = False
            self.fire_tick = 0
            self.attack = True
            self.image_key = "Attack"
            self.tick = 0
            self.fire_lock = False

        # Verifica si el jugador toco al enemigo
        player = self.level.player
        prev_bottom = player.rect.bottom + player.change_y

        if player.hit_box.colliderect(self.hit_box):
            # Si brinco encima, rebota al jugador y golpea al enemigo
            if player.change_y < 0 and player.rect.bottom >= self.hit_box.top and prev_bottom <= self.hit_box.top:
                player.change_y = (player.jumpSpeed // 2)
                player.jump(False)
                self.hit()
            else:
                if not self.level.player.hurt:
                    self.level.player.hit()
    
    def hit(self):
        """ Lastima al enemigo
        """
        self.hurt = True
        self.image_key = "Hit"
        self.idle = False
        self.tick = 0
        self.done = False
        self.hit_sound.play()