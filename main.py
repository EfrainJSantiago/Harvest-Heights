import random
import math
import pygame

#from clases.enemy import Enemy
from clases.player import Player
from clases.level import Level
from clases.start_screen import Start

import levels.flat as Flat
flat = [Flat.terrain_pos, Flat.terrain_extra_pos, Flat.solids_pos, Flat.player_start,
		Flat.tile_multiplier, Flat.tile_size, Flat.background_color, Flat.border1,
		Flat.border1_extras, Flat.border2, Flat.border2_extras, Flat.scene_terrain,
		Flat.scene_collectables]

pygame.init()

mainClock = pygame.time.Clock()

# Window
WINDOWWIDTH = 608
WINDOWHEIGHT = 416
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

player.level = current_level

current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)

# OTHER VARS
done = False

start_screen = Start(screen)

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			pass
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()

	screen.fill((0, 0, 0))
	start_screen.update()
	start_screen.draw(screen)

	mainClock.tick(60)
	pygame.display.flip()

start_screen.clear()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()

	current_level.player.move()

	current_level.draw(screen)

	mainClock.tick(FPS)
	pygame.display.flip()