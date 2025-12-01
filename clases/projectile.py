import pygame

class Projectile(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, direction, level):
        # Call the parent class (Sprite) constructor
        super().__init__()
        path = "assets/Enemies/Plant/Bullet.png"
 
        image = pygame.image.load(path).convert()
        surface = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
        rect = pygame.Rect(0, 0, 16, 16)
        surface.blit(image, (0, 0), rect)
        self.image = pygame.transform.scale2x(surface)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.sound = pygame.mixer.Sound("si_sprites_and_sounds/Projectile.aiff")

        self.direction = direction
        self.level = level
        self.moveSpeed = 6
 
    def update(self):
        """ Move the bullet.
        """
        if self.direction == 'left':
            self.rect.x -= self.moveSpeed
            if self.rect.right < 0:
                self.kill()
        else:
            self.rect.x += self.moveSpeed
            if self.rect.left > pygame.display.get_surface().get_width():
                self.kill()
        
        # Verifica si choco algo
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if len(block_hit_list) > 0:
            self.kill()

        if pygame.sprite.collide_mask(self, self.level.player):
            if not self.level.player.hurt and not self.level.player.appear:
                self.level.player.hit()
                self.kill()
    
    def fire(self):
        """ Plays Projectile's sound
        """
        #self.sound.play()