import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH, character):
        super().__init__()
        # Importar sprite sheets a ser usadas
        path = "assets/Main Characters/" + character + '/'
        images = ["Run (32x32).png",
                 "Jump (32x32).png",
                 "Fall (32x32).png",
                 "Idle (32x32).png",
                 "Fall (32x32).png",
                 "Hit (32x32).png",]
        
        self.all_sprites = {}
        self.animation_speed = 3
        self.tick = 0
        self.mask = None

        # Load Player Sprites
        for image in images:
            sprite_sheet = pygame.image.load(path + image).convert_alpha()
            sprites = []
            for i in range(sprite_sheet.get_width() // 32):
                surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * 32, 0, 32, 32)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            
            self.all_sprites[image.replace(" (32x32).png", "") + "_right"] = sprites
            flipped_sprites = sprites[:]
            for i in range(len(flipped_sprites)):
                flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
            self.all_sprites[image.replace(" (32x32).png", "") + "_left"] = flipped_sprites

        self.appear = True
        self.disappear = False

        sprite_sheet = pygame.image.load('assets/Main Characters/Appearing (96x96).png').convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // 96):
            surface = pygame.Surface((96, 96), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 96, 0, 96, 96)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        self.all_sprites["Appearing_right"] = sprites
        flipped_sprites = sprites[:]
        for i in range(len(flipped_sprites)):
            flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
        self.all_sprites["Appearing_left"] = sprites
        
        sprite_sheet = pygame.image.load('assets/Main Characters/Desappearing (96x96).png').convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // 96):
            surface = pygame.Surface((96, 96), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 96, 0, 96, 96)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        self.all_sprites["Desappearing_right"] = sprites
        flipped_sprites = sprites[:]
        for i in range(len(flipped_sprites)):
            flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
        self.all_sprites["Desappearing_left"] = sprites

        self.image = self.all_sprites["Idle_right"][0]
        self.image_key = "Idle"
        self.screenW = screenW
        self.screenH = screenH
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # Jumping variables
        self.change_x = 0
        self.moveSpeed = 6
        self.jumpSpeed = 16
        self.change_y = self.jumpSpeed
        self.gravity = 1
        self.jumping = False
        self.falling = False

        # Other
        self.level = None
        self.facingLeft = False
        self.done = False
        self.spawn_pos = None
        self.hurt = False

    def move(self):
        if self.appear or self.disappear or self.hurt:
            return
        keys = pygame.key.get_pressed()
        self.change_x = 0
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            #self.rect.x -= self.change_x
            self.change_x = -self.moveSpeed
            if not (self.jumping or self.falling):
                self.image_key = "Run"
            if not self.facingLeft:
                self.tick = 0
            self.facingLeft = True
        elif keys[pygame.K_RIGHT] and self.rect.x < self.screenW - self.rect.width:
            #self.rect.x += self.change_x
            self.change_x = self.moveSpeed
            if not (self.jumping or self.falling):
                self.image_key = "Run"
            if self.facingLeft:
                self.tick = 0
            self.facingLeft = False
        elif keys[pygame.K_r]:
            self.level.resetScene(self.level.screen, self.screenW, self.screenH)
        else:
            if self.jumping:
                self.image_key = "Jump"
            elif self.falling:
                self.image_key = "Fall"
            else:
                if not (self.appear or self.disappear or self.hurt):
                    self.image_key = "Idle"
        if keys[pygame.K_SPACE]:
            self.jump()

    def update(self):
        """ Move the player. """
        if self.done and self.disappear:
            self.kill()
        elif self.done and self.hurt:
            self.done = False
            self.despawn()
        elif self.done and self.appear:
            self.appear = False
            self.done = False
            self.rect.x = self.spawn_pos[0]
            self.rect.y = self.spawn_pos[1]
            self.image_key = "Idle"
        
        if self.hurt:
            if self.facingLeft:
                self.rect.x += 1
            else:
                self.rect.x += -1
            self.rect.y += -1
            
        if self.appear:
            self.image_key = "Appearing"
            if not self.spawn_pos:
                self.spawn_pos = (self.rect.x, self.rect.y)

        # Animation
        sprite_sheet_name = self.image_key

        if self.facingLeft:
            sprite_sheet_name += "_left"
        else:
            sprite_sheet_name += "_right"

        sprites = self.all_sprites[sprite_sheet_name]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1
        if not (self.appear or self.disappear):
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        else:
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.mask = pygame.mask.from_surface(self.image)

        if (self.disappear or self.appear or self.hurt) and sprite_index == len(sprites) - 1:
            self.done = True
        # Animation End

        if self.disappear or self.appear or self.hurt:
            return

        # See if we hit anything
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        if self.jumping or self.falling:
            self.rect.y -= self.change_y    # subir/bajar 
            self.change_y -= self.gravity         # gravedad (que tan pesado es el salto)
            if self.change_y < 0:
                if self.jumping:
                    self.tick = 0
                    self.image_key = "Fall"
                self.jumping = False
                self.falling = True

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
                self.falling = False
                self.change_y = 0
            elif self.change_y > 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0
        
        # Check and see if we land on a semisolid
        prev_bottom = self.rect.bottom + self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0 and self.rect.bottom >= block.rect.top and prev_bottom <= block.rect.top:
                self.rect.bottom = block.rect.top
                self.jumping = False
                self.falling = False
                self.change_y = 0
        
        # Check and see if we land on the end goal
        if self.level.end_goal and self.rect.colliderect(self.level.end_goal.rect):
            self.level.end_goal.trigger()
        
        # --- Check if player walked off a platform ---
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) == 0 and not self.jumping:
            if not self.falling:
                self.change_y = 0
            self.falling = True
        
        if self.rect.bottom >= self.screenH and not self.hurt:
            self.falling = False
            self.change_y = 0
            self.jumping = False
            self.hurt = True
            self.image_key = "Hit"
            self.tick = 0


    def jump(self, check = True):
        """ Called when user hits 'jump' button. """
        if not self.jumping and not self.falling:
            self.change_y = self.jumpSpeed

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screenH and check:
            if not self.jumping and not self.falling:
                self.jumping = True
                self.image_key = "Jump"
                self.tick = 0
            if self.falling:
                self.image_key = "Fall"
        elif self.rect.bottom > self.screenH and not self.hurt:
            self.falling = False
            self.change_y = 0
            self.jumping = False
            self.hurt = True
            self.image_key = "Hit"
            self.tick = 0
    
    def despawn(self):
        self.disappear = True
        self.tick = 0
        self.image_key = "Desappearing"