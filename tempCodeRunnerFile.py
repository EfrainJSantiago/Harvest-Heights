game_over = False
					player = Player(WINDOWWIDTH, WINDOWHEIGHT, character)

					# Reset Scores
					current_lives = MAX_LIVES
					timer = MAX_TIME
					freeze_frame = False
					time_out = False
					done = False

					# Comenzar desde el comienzo del nivel
					current_level.restartLevel()
					current_level.respawn_player(player)
					player.level = current_level
					
					current_level.startGame(screen, WINDOWWIDTH, WINDOWHEIGHT)