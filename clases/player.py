import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH):
        super().__init__()
        # importar imagen de saltar, caer y idle
        path = "assets/Main Characters/Ninja Frog/"
        images = ["Run (32x32).png",
                 "Jump (32x32).png",
                 "Fall (32x32).png",
                 "Idle (32x32).png",
                 "Fall (32x32).png"]
        
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

        self.image = self.all_sprites["Idle_right"][0]
        self.image_key = "Idle"
        # self.image.fill(color)
        self.screenW = screenW
        self.screenH = screenH
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # Jumping variables
        self.change_x = 6
        self.jumpSpeed = 16
        self.change_y = self.jumpSpeed
        self.gravity = 1
        self.jumping = False
        self.falling = False

        # Other
        self.level = None
        self.facingLeft = False

    def move(self):
        self.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.change_x
            if not (self.jumping or self.falling):
                self.image_key = "Run"
            if not self.facingLeft:
                self.tick = 0
            self.facingLeft = True
        elif keys[pygame.K_RIGHT] and self.rect.x < self.screenW - self.rect.width:
            self.rect.x += self.change_x
            if not (self.jumping or self.falling):
                self.image_key = "Run"
            if self.facingLeft:
                self.tick = 0
            self.facingLeft = False
        else:
            if self.jumping:
                self.image_key = "Jump"
            if self.falling:
                self.image_key = "Fall"
            else:
                self.image_key = "Idle"
            #if self.facingLeft == True:
                #self.image = pygame.transform.flip(self.img_idle, True, False)
            #else:
                #self.image = self.img_idle
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.change_y
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.change_y
        if keys[pygame.K_SPACE]:
            #self.jump()
            if not self.jumping and not self.falling:
                self.jumping = True
                self.image_key = "Jump"
                self.tick = 0
            if self.falling:
                self.image_key = "Fall"

    def update(self):
        """ Move the player. """
        #if self.facingLeft:
            #self.image = pygame.transform.flip(self.image, True, False)
        # Gravity
        #self.calc_grav()

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
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        # Animation End

        # See if we hit anything
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
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            #self.change_y = 0
            self.jumping = False
            self.falling = False
            self.change_y = self.jumpSpeed

    # def calc_grav(self):
    #     """ Calculate effect of gravity. """
    #     if self.change_y == 0:
    #         self.change_y = 1
    #     else:
    #         self.change_y += .35

    #     # See if we are on the ground.
    #     if self.rect.y >= self.screenH - self.rect.height and self.change_y >= 0:
    #         self.change_y = 0
    #         self.rect.y = self.screenH - self.rect.height

    # def jump(self):
    #     """ Called when user hits 'jump' button. """

    #     # move down a bit and see if there is a platform below us.
    #     # Move down 2 pixels because it doesn't work well if we only move down
    #     # 1 when working with a platform moving down.
    #     self.rect.y += 2
    #     platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    #     self.rect.y -= 2

    #     # If it is ok to jump, set our speed upwards
    #     if len(platform_hit_list) > 0 or self.rect.bottom >= self.screenH:
    #         self.change_y = -15