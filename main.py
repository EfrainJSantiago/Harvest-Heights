import random
import math
import pygame

#from clases.enemy import Enemy
from clases.player import Player
from clases.level import Level
from clases.start_screen import Start
from clases.npc import NPC_IDLE
from clases.fruits import Fruits

# Crear las escenas de los niveles
import levels.flat as Flat
import levels.test as Test
import levels.battlefield as Battlefield
scenes = [Battlefield.scene1, Test.scene1, Flat.scene1]

pygame.init()

# Manejar el pacing
mainClock = pygame.time.Clock()
FPS = 60

# Window
WINDOWWIDTH = 608
WINDOWHEIGHT = 416
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Harvest Heights")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Declarar el jugador
character = "Ninja Frog"
player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
player_npc = NPC_IDLE(WINDOWWIDTH, WINDOWHEIGHT, character)
MAX_LIVES = 3
current_lives = MAX_LIVES

# Logica de niveles
levels = [Level(screen, player, scenes)]
current_level_no = 0
current_level = levels[current_level_no]

player.level = current_level

current_level.startGame(screen, WINDOWWIDTH, WINDOWHEIGHT)
MAX_TIME = FPS * 60 * 2 # Tiempo en frames por segundo por minuto
timer = MAX_TIME

# Fonts
font = pygame.font.Font("BoldPixels.otf", 36) #28
font_outline = pygame.font.Font("BoldPixels.otf", 40)
font_timer = pygame.font.Font("BoldPixels.otf", 38)
font_shadow = pygame.font.Font("BoldPixels.otf", 37)

# Estados de juego
done = False # Menu y transición de niveles
game_over = False # Game Over
game_complete = False # Completo el juego

# Otras Variables
freeze_frame = False
time_out = False
play_again = False
lives_lock = False
level_complete = False
fruit = Fruits("Apple")
all_sprites = pygame.sprite.Group()
all_sprites.add(player_npc)
all_sprites.add(fruit)

# Musica y Sonido


# In between background
TILES = []
background = pygame.image.load("assets/Background/Purple.png").convert()
_, _, width, height = background.get_rect()

# Adds background
for i in range(WINDOWWIDTH // width + 1):
	for j in range(WINDOWHEIGHT // height + 1):
		pos = (i * width, j * height)
		TILES.append(pos)

def draw_background():
	for tile in TILES:
		screen.blit(background, tile)

# Crea el menu de inicio
start_screen = Start(screen)

# Logica de menu
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
			if event.key == pygame.K_RETURN:
				done = True

	screen.fill((0, 0, 0))
	start_screen.update()
	start_screen.draw(screen)

	# Actualiza el estado del juego
	mainClock.tick(60)
	pygame.display.flip()

start_screen.clear()

# Inicia el estado de transición al primer nivel
done = False

# Logica de juego
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
			# Debugging {Please remove when done}
			elif event.key == pygame.K_BACKSPACE and timer > 600:
				timer = 600
			
		# Verifica inputs adicionales en caso de game over
		if event.type == pygame.KEYDOWN and game_over:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				play_again = not play_again
			if event.key == pygame.K_RETURN:
				if play_again == False:
					pygame.quit()
					quit()
				elif play_again == True: # Reset Game
					gameover = False
					player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)

					# Reset Scores
					current_lives = MAX_LIVES
					timer = MAX_TIME
					freeze_frame = False
					time_out = False
					player.level = current_level

					# Comenzar desde el comienzo del nivel
					current_level.restartLevel(screen, WINDOWWIDTH, WINDOWHEIGHT)
	
	# Si el nivel no esta listo, preparalo
	if not done:
		# Si no ha completado el ultimo nivel, prepara el proximo
		if level_complete and current_level_no != len(levels) - 1:
			current_level.clear()
			current_level_no += 1
			current_level = levels[current_level_no]

			player.level = current_level

			current_level.startGame(screen, WINDOWWIDTH, WINDOWHEIGHT)
			level_complete = False
		# Si completo el ultimo nivel, gano el juego
		elif level_complete and current_level_no == len(levels) - 1:
			game_complete = True
			done = True
		elif not level_complete: # Transición al proximo nivel
			if timer == MAX_TIME:
				timer = 180
			elif timer > 0:
				# Tiempo de espera
				timer -= 1

				# Dibuja la pantalla de transición
				draw_background()
				y_offset = (WINDOWHEIGHT // 2) - 30

				text = font.render('Level ' + str(current_level_no + 1), True, WHITE)
				textRect = text.get_rect()
				textRect.topleft = (50, y_offset - (textRect.height // 2))
				textRect.centerx = screen.get_rect().centerx
				screen.blit(text, textRect)

				y_offset += 60

				text = font.render('Lives: ' + str(current_lives), True, WHITE)
				textRect = text.get_rect()
				textRect.topleft = (50, y_offset - (textRect.height // 2))
				textRect.centerx = screen.get_rect().centerx
				screen.blit(text, textRect)
			else: # Si se acabo el tiempo de espera, entra al nivel
				done = True
				timer = MAX_TIME
	# Si no obtuvo un game over o completo el juego, entra al juego
	elif not game_over and not game_complete:
		current_level.player.move()
		current_level.collect()
		current_level.checkComplete()

		current_level.update()
		current_level.draw(screen)

		# Si completo el nivel, señalalo
		if current_level.checkFinished():
			if not level_complete:
				timer = 60
				level_complete = True
			elif timer > 0:
				timer -= 1
			elif timer == 0:
				done = False
				timer = MAX_TIME
		# Si completo una escena y no es la ultima, pasa a la proxima
		elif current_level.checkComplete() and not player.alive() and not current_level.end_goal:
			player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
			current_level.respawn_player(player)
			player.level = current_level
			current_level.progress(screen, WINDOWWIDTH, WINDOWHEIGHT)
		# Si el jugador murio y no se ha acabado el tiempo
		elif not player.alive() and not time_out:
			# Baja la vida
			if not lives_lock:
				current_lives -= 1
				lives_lock = True
			# Si todavia tiene vidas, crea un nuevo jugador y reinicia la escena
			if current_lives != 0:
				player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
				current_level.respawn_player(player)
				player.level = current_level
				current_level.resetScene(screen, WINDOWWIDTH, WINDOWHEIGHT)
				lives_lock = False
			# Si perdio todas las vidas, Game Over
			else:
				game_over = True
				lives_lock = False
				timer = 60
		# Si se acabo el tiempo, Game Over
		elif timer <= 0:
			# Golpea al jugador para iniciar su desaparición
			if not player.hurt:
				player.falling = False
				player.change_y = 0
				player.jumping = False
				player.hurt = True
				player.image_key = "Hit"
				player.tick = 0
				time_out = True
			# Si no se ha parado el juego luego del golpe, paralo
			if not freeze_frame and (player.image == player.all_sprites["Hit_right"][0]
								 	or player.image == player.all_sprites["Hit_left"][0]):
				pygame.time.wait(1000)
				freeze_frame = True
			# Si el jugador murio, Game Over
			if not player.alive():
				game_over = True
				timer = 60
		
		# Escribe el numero de vidas actual en la pantalla
		outline = font_outline.render(str(current_lives), True, BLACK)
		screen.blit(outline, [10, 10])
		text = font.render(str(current_lives), True, WHITE)
		screen.blit(text, [10, 10])

		# Calcula el tiempo sobrante del nivel
		seconds = timer // 60
		minutes = seconds // 60
		seconds = seconds % 60
		current_time = str(minutes) + ':'
		if seconds < 10:
			current_time += "0" + str(seconds)
		else:
			current_time += str(seconds)

		# Escribe el tiempo actual en la pantalla
		outline = font_timer.render(str(current_time), True, BLACK)
		screen.blit(outline, [WINDOWWIDTH - 5 - outline.get_rect().width, 10])
		text = font.render(str(current_time), True, WHITE)
		screen.blit(text, [WINDOWWIDTH - 10 - text.get_rect().width, 10])

		# Reduce el tiempo del nivel
		if timer > 0:
			timer -= 1
	# Si es game over, entra a la pantalla de Game Over
	elif game_over:
		# Tiempo de espera
		if timer > 0:
			timer -= 1
			current_level.update()
			current_level.draw(screen)
		else:
			# Dibuja la pantalla de Game Over
			draw_background()
			y_offset = (WINDOWHEIGHT // 2) - 90

			text = font.render('Game Over', True, WHITE)
			textRect = text.get_rect()
			textRect.topleft = (50, y_offset)
			textRect.centerx = screen.get_rect().centerx
			screen.blit(text, textRect)
			
			y_offset += 90
			text = font.render('Play Again?', True, WHITE)
			textRect = text.get_rect()
			textRect.topleft = (50, y_offset)
			textRect.centerx = screen.get_rect().centerx
			screen.blit(text, textRect)

			y_offset += 60
			text = font.render('Yes', True, WHITE)
			yestextRect = text.get_rect()
			yestextRect.topleft = (screen.get_rect().centerx - yestextRect.width - 50, y_offset)
			screen.blit(text, yestextRect)

			text = font.render('No', True, WHITE)
			textRect = text.get_rect()
			textRect.topleft = (screen.get_rect().centerx + 50, y_offset)
			screen.blit(text, textRect)

			# Custom cursor display
			yesBox = screen.get_rect().centerx - yestextRect.width - 50

			y_offset += (textRect.height // 2)
			
			# Moves Cursor
			if play_again:
				select_triangle = [(yesBox - 15, y_offset), (yesBox - 30, y_offset - 15), (yesBox - 30, y_offset + 15)]
			else:
				select_triangle = [(screen.get_rect().centerx + 35, y_offset),
									(screen.get_rect().centerx + 20, y_offset - 15),
									(screen.get_rect().centerx + 20, y_offset + 15)]
			
			# Draws cursor
			pygame.draw.polygon(screen, WHITE, select_triangle)
	# Si gano el juego, entra a la pantalla de 'coronamiento'
	elif game_complete:
		draw_background()
		y_offset = (WINDOWHEIGHT // 2) - 30

		player_npc.rect.bottom = y_offset
		player_npc.rect.right = (WINDOWWIDTH // 2) - 10
		fruit.rect.bottom = y_offset
		fruit.rect.left = (WINDOWWIDTH // 2) + 10

		all_sprites.update()
		all_sprites.draw(screen)

		y_offset += 60

		text = font.render('A WINNER IS YOU', True, WHITE)
		textRect = text.get_rect()
		textRect.topleft = (50, y_offset)
		textRect.centerx = screen.get_rect().centerx
		screen.blit(text, textRect)

	# Actualiza el estado del juego
	mainClock.tick(FPS)
	pygame.display.flip()