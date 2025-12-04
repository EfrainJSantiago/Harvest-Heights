import pygame

from clases.player import Player
from clases.level import Level
from clases.start_screen import Start
from clases.npc import NPC_IDLE
from clases.fruits import Fruits

# Crear las escenas de los niveles
import levels.level1 as Level1
import levels.level2 as Level2
import levels.level3 as Level3

level1_music = Level1.music
level2_music = Level2.music
level3_music = Level3.music
level1_scenes = [Level1.scene1, Level1.scene2, Level1.scene3, Level1.scene4, Level1.scene5]
level2_scenes = [Level2.scene1, Level2.scene2, Level2.scene3, Level2.scene4, Level2.scene5]
level3_scenes = [Level3.scene1, Level3.scene2, Level3.scene3, Level3.scene4, Level3.scene5]

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

# Vidas
MAX_LIVES = 3
current_lives = MAX_LIVES

# Logica de niveles
levels = [Level(screen, player, level1_scenes, level1_music),
		  Level(screen, player, level2_scenes, level2_music),
		  Level(screen, player, level3_scenes, level3_music)]
current_level_no = 0
current_level = levels[current_level_no]
player.level = current_level
current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)

# Tiempo
MAX_TIME = FPS * 60 * 2 	# Tiempo en frames por segundo por minuto
timer = MAX_TIME
time = timer
tick_down = True

# Fonts
font = pygame.font.Font("BoldPixels.otf", 36) #28
font_outline = pygame.font.Font("BoldPixels.otf", 40)
font_timer = pygame.font.Font("BoldPixels.otf", 38)
font_shadow = pygame.font.Font("BoldPixels.otf", 37)

# Estados de juego
done = False 			# Menu y transición de niveles
game_over = False 		# Game Over
game_complete = False 	# Completo el juego
paused = False 			# Alterna el estado del juego entre juego y pausa.

# Variables del Win Screen
player_npc = NPC_IDLE(WINDOWWIDTH, WINDOWHEIGHT, character)
fruit = Fruits("Apple")
all_sprites = pygame.sprite.Group()
all_sprites.add(player_npc)
all_sprites.add(fruit)

# Otras Variables
freeze_frame = False 	# Detiene la pantalla
time_out = False 		# Determina si se acabo el tiempo
play_again = False 		# Determina si el jugador quiere jugar otra vez
lives_lock = False 		# Evita que las vidas sean restadas cada frame
level_complete = False 	# Determina si el nivel ha sido completado
music_loaded = False 	# Determina si se puede cambiar la musica

# Musica y Sonido
transition = pygame.mixer.Sound("sounds/Retro Event Acute 08.wav")
pause = pygame.mixer.Sound("sounds/Retro Event StereoUP 02.wav") # or Retro Event UI 01
pygame.mixer.music.load("sounds/music/Troubadeck 28 Quaint Questions.ogg")
transition.set_volume(0.5)
pause.set_volume(0.2)
pygame.mixer.music.set_volume(0.7)

# Fondo Principal
TILES = []
background = pygame.image.load("assets/Background/Purple.png").convert()
_, _, width, height = background.get_rect()

	# Crea el background
for i in range(WINDOWWIDTH // width + 1):
	for j in range(WINDOWHEIGHT // height + 1):
		pos = (i * width, j * height)
		TILES.append(pos)

def draw_background():
	""" Dibuja el fondo a la pantalla
	"""
	for tile in TILES:
		screen.blit(background, tile)

# Menu de Inicio
start_screen = Start(screen)
pygame.mixer.music.play(-1, fade_ms=1000)

# Logica de menu
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			done = True
			transition.play()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				done = True
				transition.play()

	screen.fill((0, 0, 0))
	start_screen.update()
	start_screen.draw(screen)

	mainClock.tick(60)
	pygame.display.flip()

start_screen.clear()
pygame.mixer.music.fadeout(2000)

# Inicia el estado de transición al primer nivel
done = False

# Logica de juego
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			# Alterna el estado de juego
			if event.key == pygame.K_ESCAPE:
				if not game_complete and not game_over and done:
					paused = not paused
					if paused:
						pause.play()
						current_level.pause_music()
					elif not paused:
						current_level.unpause_music()
			
		# Verifica inputs adicionales en caso de game over
		if event.type == pygame.KEYDOWN and game_over:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				play_again = not play_again
			if event.key == pygame.K_RETURN:
				if not play_again:
					pygame.quit()
					quit()
				
				# Reinicia el nivel
				elif play_again:
					transition.play()
					pygame.mixer.music.fadeout(1000)

					# Reinicia valores
					music_loaded = False
					game_over = False
					current_lives = MAX_LIVES
					timer = MAX_TIME
					freeze_frame = False
					time_out = False
					done = False
					tick_down = True

					# Comenzar desde el comienzo del nivel
					player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
					current_level.restartLevel()
					current_level.respawn_player(player)
					player.level = current_level
					current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)
	
	# Si el nivel no esta listo, preparalo
	if not done:
		# Si no ha completado el ultimo nivel, prepara el proximo
		if level_complete and current_level_no != len(levels) - 1:
			current_level.clear()
			current_level_no += 1
			current_level = levels[current_level_no]

			player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
			player.level = current_level
			current_level.respawn_player(player)

			lives_lock = False
			time_out = False

			current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)
			level_complete = False

		# Si completo el ultimo nivel, gano el juego
		elif level_complete and current_level_no == len(levels) - 1:
			game_complete = True
			done = True

		# Transición al proximo nivel
		elif not level_complete:
			if timer == MAX_TIME:
				# Tiempo de espera
				timer = 180
				if current_level_no != 0:
					transition.play()
			elif timer > 0:
				if timer <= 180:
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
			
			# Si se acabo el tiempo de espera, entra al nivel
			else:
				pygame.mixer.music.stop()
				pygame.mixer.music.unload()
				current_level.load_music()
				done = True
				timer = MAX_TIME
				tick_down = True
	
	# Si no obtuvo un game over o completo el juego, entra al juego
	elif not game_over and not game_complete:

		# Si el juego no esta pausado, sigue de costumbre
		if not paused:
			if not music_loaded and not (game_over or level_complete):
				current_level.play_music()
				music_loaded = True
			current_level.player.action()
			current_level.collect()
			current_level.checkComplete()

			current_level.update()
			current_level.draw(screen)

			# Si completo el nivel, señalalo
			if current_level.checkFinished():
				if not level_complete:
					timer = 60
					level_complete = True
					tick_down = False
				elif timer > 0:
					timer -= 1
				elif timer == 0:
					done = False
					timer = MAX_TIME
				if music_loaded:
					pygame.mixer.music.fadeout(500)
					music_loaded = False

			# Si completo una escena y no es la ultima, pasa a la proxima
			elif current_level.checkComplete() and not player.alive() and not current_level.end_goal:
				player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)
				current_level.respawn_player(player)
				player.level = current_level
				current_level.progress(WINDOWWIDTH, WINDOWHEIGHT)

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
					current_level.resetScene(WINDOWWIDTH, WINDOWHEIGHT)
					lives_lock = False

				# Si perdio todas las vidas, Game Over
				else:
					game_over = True
					lives_lock = False
					timer = 60
					tick_down = False
					if music_loaded:
						pygame.mixer.music.fadeout(500)
						music_loaded = False

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
					if music_loaded:
						pygame.mixer.music.fadeout(500)
						music_loaded = False

				# Si el jugador murio, Game Over
				if not player.alive():
					game_over = True
					timer = 60
					tick_down = False
		else:
			current_level.draw(screen)

			# Oscurece la pantalla
			black_Transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
			black_Transparent_surface.fill((0, 0, 0, 150))
			screen.blit(black_Transparent_surface, (0, 0))

			# Escribe PAUSED a la pantalla
			pause_text = font.render("PAUSED", True, WHITE)
			rect = pause_text.get_rect(center=(WINDOWWIDTH//2, WINDOWHEIGHT//2))
			screen.blit(pause_text, rect)
		
		# Escribe el numero de vidas actual en la pantalla
		outline = font_outline.render(str(current_lives), True, BLACK)
		screen.blit(outline, [10, 10])
		text = font.render(str(current_lives), True, WHITE)
		screen.blit(text, [10, 10])

		# Calcula el tiempo sobrante del nivel
		if tick_down:
			time = timer
		seconds = time // 60
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

		# Reduce el tiempo del nivel si el juego no esta pausado
		if timer > 0 and not paused and not level_complete:
			timer -= 1

	# Si es game over, entra a la pantalla de Game Over
	elif game_over:

		# Tiempo de espera
		if timer > 0:
			timer -= 1
			current_level.update()
			current_level.draw(screen)
		else:
			if not music_loaded:
				pygame.mixer.music.load("sounds/music/Sketchbook 2024-11-20.ogg")
				pygame.mixer.music.set_volume(0.5)
				pygame.mixer.music.play(-1, fade_ms=1000)
				music_loaded = True

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
		if not music_loaded:
				pygame.mixer.music.load("sounds/music/Troubadeck 12 Good King.ogg")
				pygame.mixer.music.set_volume(0.7)
				pygame.mixer.music.play(-1, fade_ms=1000)
				music_loaded = True

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
	
	mainClock.tick(FPS)
	pygame.display.flip()