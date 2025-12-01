import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH, character):
        super().__init__()
        # Guarda el tamaño de la pantalla
        self.screenW = screenW
        self.screenH = screenH

        # Importar sprite sheets a ser usadas
        path = "assets/Main Characters/" + character + '/'
        images = ["Run (32x32).png",
                 "Jump (32x32).png",
                 "Fall (32x32).png",
                 "Idle (32x32).png",
                 "Fall (32x32).png",
                 "Hit (32x32).png",]

        # Carga todos los sprites del jugador.
        self.all_sprites = {}
        for image in images:
            # Carga el sprite sheet
            sprite_sheet = pygame.image.load(path + image).convert_alpha()
            sprites = []

            # Por cada sprite en el sprite sheet, crea una instancia del sprite
            for i in range(sprite_sheet.get_width() // 32):
                surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * 32, 0, 32, 32)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            
            # Guarda todos los sprites en su direccion default.
            self.all_sprites[image.replace(" (32x32).png", "") + "_right"] = sprites

            # Guarda todos los sprites en su direccion opuesta.
            flipped_sprites = sprites[:]
            for i in range(len(flipped_sprites)):
                flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
            self.all_sprites[image.replace(" (32x32).png", "") + "_left"] = flipped_sprites

        # Carga el sprite sheet de aparecer
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
        
        # Carga el sprite sheet de aparecer
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

        # Asigna un sprite por default
        self.image = self.all_sprites["Idle_right"][0]
        self.image_key = "Idle"
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_box = pygame.Rect(0, 0, 46, 48)

        # Variables para animación
        self.animation_speed = 3
        self.tick = 0
        self.done = False

        # Variables para status del jugador
        self.appear = True
        self.disappear = False
        self.hurt = False
        self.facingLeft = False

        # Variables de salto
        self.change_x = 0
        self.moveSpeed = 6
        self.jumpSpeed = 16
        self.change_y = self.jumpSpeed
        self.gravity = 1
        self.jumping = False
        self.falling = False

        # Variables de sonido
        self.hop = pygame.mixer.Sound("sounds/Retro Jump Classic 08.wav")
        self.hop.set_volume(0.2)
        self.hit_sound = pygame.mixer.Sound("sounds/Retro Negative Short 23.wav")
        self.hit_sound.set_volume(0.2)

        # Other
        self.level = None
        self.spawn_pos = None

    def action(self):
        """ Obtiene el input del jugador
        """
        if self.appear or self.disappear or self.hurt:
            return
        
        keys = pygame.key.get_pressed()
        self.change_x = 0

        # Si no se tocan las teclas de direcciones o hay conflicto entre ellas,
        # el jugador se queda en su lugar
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) or (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
            if self.jumping:
                self.image_key = "Jump"
            elif self.falling:
                self.image_key = "Fall"
            else:
                if not (self.appear or self.disappear or self.hurt):
                    self.image_key = "Idle"
        else:
            # Movimiento a la izquierda
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.change_x -= self.moveSpeed
                if not (self.jumping or self.falling):
                    self.image_key = "Run"
                if not self.facingLeft:
                    self.tick = 0
                self.facingLeft = True
            
            # Movimiento a la derecha
            if keys[pygame.K_RIGHT] and self.rect.x < self.screenW - self.rect.width:
                self.change_x += self.moveSpeed
                if not (self.jumping or self.falling):
                    self.image_key = "Run"
                if self.facingLeft:
                    self.tick = 0
                self.facingLeft = False
        
        # Salto
        if keys[pygame.K_SPACE]:
            self.jump()

    def update(self):
        """ Actualiza el estado del jugador.
        """

        # Verifica si una animación llego a su final
        if self.done:
            # Si es la de desaparecer, matalo
            if self.disappear:
                self.kill()
            # Si es la de golpe, desaparece
            if self.hurt:
                self.done = False
                self.despawn()
            # Si es la de aparecer, inicia la animacion de idle
            if self.appear:
                self.appear = False
                self.done = False
                self.rect.x = self.spawn_pos[0]
                self.rect.y = self.spawn_pos[1]
                self.image_key = "Idle"
        
        # Si fue golpeado, eleva al jugador
        if self.hurt:
            if self.facingLeft:
                self.rect.x += 1
            else:
                self.rect.x += -1
            self.rect.y += -1
        
        # Si esta apareciendo, señalalo, y guarda la posición inicial
        if self.appear:
            self.image_key = "Appearing"
            if not self.spawn_pos:
                self.spawn_pos = (self.rect.x, self.rect.y)

        self.animate()

        if self.disappear or self.appear or self.hurt:
            return

        # Verifica si chocamos algo
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Si nos estamos moviendo a la derecha,
            # asigna nuestra derecha a la izquierda del objeto que chocamos.
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # De lo contrario, si nos estamos moviendo a la izquierda, haz lo opuesto.
                self.rect.left = block.rect.right

        # Movimiendo de arriba/abajo
        if self.jumping or self.falling:
            self.rect.y -= self.change_y
            self.change_y -= self.gravity
            if self.change_y < 0:
                if self.jumping:
                    self.tick = 0
                    self.image_key = "Fall"
                self.jumping = False
                self.falling = True

        self.hit_box.bottom = self.rect.bottom
        self.hit_box.centerx = self.rect.centerx

        # Verifica si choco algo
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reinicia nuestra posición en base al tope/fondo del objeto
            if self.change_y < 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
                self.falling = False
                self.change_y = 0
            elif self.change_y > 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0
        
        # Verifica si chocamos un semisolido
        prev_bottom = self.rect.bottom + self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        for block in block_hit_list:
            
            # Reinicia nuestro posición en base al tope del semisolido
            if self.change_y < 0 and self.rect.bottom >= block.rect.top and prev_bottom <= block.rect.top:
                self.rect.bottom = block.rect.top
                self.jumping = False
                self.falling = False
                self.change_y = 0
        
        # Verifica si tocamos el objetivo final
        if self.level.end_goal and self.level.end_goal.mask and pygame.sprite.collide_mask(self, self.level.end_goal):
            self.level.end_goal.trigger()
        
        # Verifica si nos bajamos de una plataforma
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        self.rect.y -= 2

        # Si no encontramos una plataforma, gira nos caemos
        if len(platform_hit_list) == 0 and not self.jumping:
            if not self.falling:
                self.change_y = 0
            self.falling = True
        
        # Si el llegamos al vacio al fondo de la pantalla, cuentalo como golpe
        if self.rect.bottom >= self.screenH and not self.hurt:
            self.hit()


    def jump(self, check = True):
        """ Se llama cuando el usuario presiona el botón "saltar".
        """
        if not self.jumping and not self.falling:
            self.change_y = self.jumpSpeed

        # Nos movemos un poco hacia abajo y comprobamos si hay una plataforma debajo.
        # Nos movemos 2 píxeles hacia abajo, ya que no funciona bien si solo nos movemos hacia abajo.
        # 1 al trabajar con una plataforma que se mueve hacia abajo.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False) + pygame.sprite.spritecollide(self, self.level.semisolid_list, False)
        self.rect.y -= 2

        # Si está bien saltar, establecemos nuestra velocidad hacia arriba
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screenH and check:
            if not self.jumping and not self.falling:
                self.jumping = True
                self.hop.play()
                self.image_key = "Jump"
                self.tick = 0
            if self.falling:
                self.image_key = "Fall"
        elif self.rect.bottom > self.screenH and not self.hurt:
            self.hit()
        elif not check:
            self.jumping = True
            if self.change_y == self.jumpSpeed:
                self.hop.play()
            self.image_key = "Jump"
            self.tick = 0
    
    def animate(self):
        """ Anima el sprite del jugador.
        """
        # Consigue el nombre del sprite para la animación
        sprite_sheet_name = self.image_key

        if self.facingLeft:
            sprite_sheet_name += "_left"
        else:
            sprite_sheet_name += "_right"

        # Actualiza el sprite del jugador para la animarlo.
        sprites = self.all_sprites[sprite_sheet_name]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1
        self.mask = pygame.mask.from_surface(self.image)

        # Si estamos desapareciendo o apareciendo, centraliza la posicion del rectangulo
        # en lugar de posicionarlo a la esquina izquierda arriba de la imagen.
        if self.appear or self.disappear:
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        else:
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        # Si la animacion del enemigo llega al final, señalalo
        if (self.disappear or self.appear or self.hurt) and sprite_index == len(sprites) - 1:
            self.done = True
    
    def hit(self):
        """ Inicia el ciclo de golpe
        """
        self.falling = False
        self.change_y = 0
        self.jumping = False
        self.hurt = True
        self.image_key = "Hit"
        self.tick = 0
        self.hit_sound.play()
    
    def despawn(self):
        """ Inicia el ciclo de desaparición.
        """
        self.disappear = True
        self.tick = 0
        self.image_key = "Desappearing"