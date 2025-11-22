import random
import math
import pygame

#from clases.enemy import Enemy
from clases.player import Player
from clases.level import Level

pygame.init()

mainClock = pygame.time.Clock()

# Window
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Harvest Heights")

WHITE = (255, 255, 255)

FPS = 60

player = Player(WINDOWWIDTH, WINDOWHEIGHT)
x_speed = 2
y_speed = 2

levels = [Level(screen, player, "Blue"), Level(screen, player, "Yellow"), Level(screen, player, "Pink")]
current_level_no = 0
current_level = levels[current_level_no]

current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    current_level.draw(screen)

    mainClock.tick(FPS)
    pygame.display.flip()