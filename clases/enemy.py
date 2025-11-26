# Programa que crea un enemigos que se mueven y enemigos que disparan

import pygame
from pygame.locals import *

# Clase para enemigos que se mueven 
class Enemy:
    def __init__(self, x, y, image_path):
        
        # Imagen mirando a la derecha
        self.image_right = pygame.image.load(image_path)
        self.image_right = pygame.transform.scale(self.image_right, (70, 50))
        
        # Imagen mirando a la izquierda (volteada horizontalmente)
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        # Empezamos mirando a la derecha
        self.image = self.image_right

        # Rectangulo que representa la posicion y tamano del enemigo 
        self.rect = self.image.get_rect()       # Crea un rectangulo que contiene la imagen
        self.rect.center = (x, y)               # Posicion del enemigo

        self.speed = 2  # derecha = positivo, izquierda = negativo


    def update(self):

        self.rect.x -= self.speed    # Mover el enemigo horizontalmente

        # ----- Rebotes -----
        if self.rect.left <= 0:     # Si toca el borde izquierdo
            self.rect.left = 0
            self.speed *= -1        # Cambia la direccion

        # elif self.rect.right >= screen_width:    # Si toca el borde derecho
        #     self.rect.right = screen_width
        #     self.speed *= -1                     # Cambia la direccion

        # ----- Elegir imagen según dirección -----
        if self.speed > 0:      # Va hacia la derecha
            self.image = self.image_right
        else:                   # Va hacia la izquierda
            self.image = self.image_left