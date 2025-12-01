import pygame
from pygame.locals import *
import os
import re

# Clase para enemigos que se mueven 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()

        # Obtiene la dirección de los tipos de animaciones del enemigo.
        path = "assets/Enemies/" + enemy_type + '/'
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        # Carga todos los sprites del enemigo.
        self.all_sprites = {}
        for image in images:
            # Carga el sprite sheet
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()
            sprites = []

            # Asigna tamaño por default (Principalmente por los bullets)
            width, height = 16, 16
            str_to_remove = None

            # Busca si el nombre del sprite tiene las dimensiones
            dimensions = self.extract_dimensions(image)
            if dimensions == None:
                str_to_remove = '.png'
                if enemy_type == 'Mushroom':
                    width, height = 32, 32
            else: # Si las tiene, remplaza los valores default
                width, height = list(dimensions)
                str_to_remove = " " + image.split()[len(image.split()) - 1]
            
            # Por cada sprite en el sprite sheet, crea una instancia del sprite
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            
            # Guarda todos los sprites en su direccion default.
            self.all_sprites[image.replace(str_to_remove, "") + "_left"] = sprites

            # Guarda todos los sprites en su direccion opuesta.
            flipped_sprites = sprites[:]
            for i in range(len(flipped_sprites)):
                flipped_sprites[i] = pygame.transform.flip(flipped_sprites[i], True, False)
            self.all_sprites[image.replace(str_to_remove, "") + "_right"] = flipped_sprites

        # Valores para calcular choque
        self.rect = None
        self.mask = None
        self.image_key = None

        # Valores para animación
        self.animation_speed = 3
        self.tick = 0
        self.done = False

        # Valores para el status del enemigo
        self.hurt = False
        self.idle = True
        self.turnLock = False

        # Otros valores
        self.level = None # Guarda el nivel donde se encuentra el enemigo
        self.moveSpeed = 2
        self.hit_sound = pygame.mixer.Sound("sounds/Retro Negative Short 23.wav")
        self.hit_sound.set_volume(0.2)

    def update(self):
        """ Actualiza la animación del enemigo.
        """
        # Consigue el nombre del sprite para la animación
        sprite_sheet_name = self.image_key

        if self.moveSpeed > 0:
            sprite_sheet_name += "_right"
        else:
            sprite_sheet_name += "_left"

        # Actualiza el sprite del enemigo para la animarlo.
        sprites = self.all_sprites[sprite_sheet_name]
        sprite_index = (self.tick // self.animation_speed) % len(sprites)
        self.image = sprites[sprite_index]
        self.tick += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Si la animacion del enemigo llega al final, señalalo
        if sprite_index == len(sprites) - 1:
            self.done = True
    
    def extract_dimensions(self, filename):
        """ Consigue las dimensiones dentro del nombre del archivo
        """
        match = re.search(r"\((\d+)x(\d+)\)", filename)
        if not match:
            return None
        return int(match.group(1)), int(match.group(2))