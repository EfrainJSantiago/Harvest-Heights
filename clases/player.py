import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH):
        super().__init__()
        # importar imagen de saltar, caer y idle
        self.img_run = pygame.image.load("assets/Main Characters/Ninja Frog/Run (32x32).png").convert_alpha()
        self.img_run = pygame.transform.scale(self.img_run, (50, 50))

        self.img_jump = pygame.image.load("assets/Main Characters/Ninja Frog/Jump (32x32).png").convert_alpha()
        self.img_jump = pygame.transform.scale(self.img_jump, (50, 50))

        self.img_fall = pygame.image.load("assets/Main Characters/Ninja Frog/Fall (32x32).png").convert_alpha()
        self.img_fall = pygame.transform.scale(self.img_fall, (50, 50))

        self.img_idle = pygame.image.load("assets/Main Characters/Ninja Frog/Idle (32x32).png").convert_alpha()
        self.img_idle = pygame.transform.scale(self.img_idle, (50, 50))
        self.image = self.img_idle
        # self.image.fill(color)
        self.screenW = screenW
        self.screenH = screenH
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.change_x = 6
        self.change_y = 6
        self.level = None
        self.facingLeft = False

    def move(self):
    #     self.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.change_x
            self.image = self.img_run
            self.facingLeft = True
        elif keys[pygame.K_RIGHT] and self.rect.x < self.screenW:
            self.rect.x += self.change_x
            self.image = self.img_run
            self.facingLeft = False
        else:
            self.image = self.img_idle
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.change_y
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.change_y
    #     if keys[pygame.K_SPACE]:
    #         self.jump()

    def update(self):
    #     """ Move the player. """
        if self.facingLeft:
            self.image = pygame.transform.flip(self.image, True, False)
    #     # Gravity
    #     self.calc_grav()

    #     # See if we hit anything
    #     block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    #     for block in block_hit_list:
    #         # If we are moving right,
    #         # set our right side to the left side of the item we hit
    #         if self.change_x > 0:
    #             self.rect.right = block.rect.left
    #         elif self.change_x < 0:
    #             # Otherwise if we are moving left, do the opposite.
    #             self.rect.left = block.rect.right

    #     # Move up/down
    #     self.rect.y += self.change_y

    #     # Check and see if we hit anything
    #     block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    #     for block in block_hit_list:

    #         # Reset our position based on the top/bottom of the object.
    #         if self.change_y > 0:
    #             self.rect.bottom = block.rect.top
    #         elif self.change_y < 0:
    #             self.rect.top = block.rect.bottom

    #         # Stop our vertical movement
    #         self.change_y = 0

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