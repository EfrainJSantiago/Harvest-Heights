import random
import math
import pygame

#from clases.enemy import Enemy
from clases.player import Player
from clases.level import Level
from clases.start_screen import Start

import levels.flat as Flat
import levels.test as Test
import levels.battlefield as Battlefield
scenes = [Battlefield.scene1, Test.scene1, Flat.scene1]

pygame.init()

mainClock = pygame.time.Clock()

# Window
WINDOWWIDTH = 608
WINDOWHEIGHT = 416
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Harvest Heights")

WHITE = (255, 255, 255)

FPS = 60

character = "Ninja Frog"
player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
x_speed = 2
y_speed = 2

levels = [Level(screen, player, scenes)]
current_level_no = 0
current_level = levels[current_level_no]

player.level = current_level

current_level.startGame(screen, WINDOWWIDTH, WINDOWHEIGHT)

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
	current_level.collect()
	current_level.checkComplete()

	current_level.draw(screen)

	if current_level.checkFinished():
		print('Complete')
		# Expand This
	elif current_level.checkComplete() and not player.alive() and not current_level.end_goal:
		# Implement Wait Here
		player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
		current_level.respawn_player(player)
		player.level = current_level
		current_level.progress(screen, WINDOWWIDTH, WINDOWHEIGHT)
	elif not player.alive():
		# Implement Wait Here
		player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
		current_level.respawn_player(player)
		player.level = current_level
		current_level.resetScene(screen, WINDOWWIDTH, WINDOWHEIGHT)

	mainClock.tick(FPS)
	pygame.display.flip()