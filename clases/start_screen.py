import pygame
from clases.terrain import Terrain
from clases.fruits import Fruits

# Variables de terreno
terrain_pos = (96, 0)
terrain_extra_pos = (144, 0)

# Otras variables
tile_multiplier = 16
tile_size = 32

# Guarda el diseño de la escena
scene_terrain = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 1, 2, 13, 5, 12, 2, 3, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 2, 13, 5, 5, 5, 5, 5, 12, 2, 3, 0, 0, 0, 0],
				[0, 0, 1, 2, 13, 5, 5, 5, 5, 5, 5, 5, 5, 5, 12, 2, 3, 0, 0],
				[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
				[7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9],]

# Guarda las frutas de la escena
fruit_pos = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

class Start:
	def __init__(self, screen):
		# Listas de sprites
		self.collectables = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()
		self.platform_list = pygame.sprite.Group()

		# Variables de texto
		self.font_title = pygame.font.Font("BoldPixels.otf", 44)
		self.font_outline = pygame.font.Font("BoldPixels.otf", 45)
		self.font = pygame.font.Font("BoldPixels.otf", 28)

		# Carga el fondo del background
		self.background = pygame.image.load("assets/Background/Blue.png").convert()
		_, _, width, height = self.background.get_rect()
		self.tiles = []

		screenW, screenH = screen.get_size()

		# Crea el background
		for i in range(screenW // width + 1):
			for j in range(screenH // height + 1):
				pos = (i * width, j * height)
				self.tiles.append(pos)
		
		# Crea y posiciona el terreno en la escena
		for row in range(len(scene_terrain)):
			for col in range(len(scene_terrain[row])):
				tile_id = scene_terrain[row][col]
				if tile_id == 0:
					continue
				
				pos_x = col * tile_size
				pos_y = row * tile_size

				tile_offset_x, tile_offset_y = self.getTilePosition(tile_id)

				terrain = Terrain(pos_x, pos_y, tile_size, tile_offset_x, tile_offset_y)
				self.platform_list.add(terrain)
		
		# Crea y posiciona las frutas en la escena
		for row in range(len(fruit_pos)):
			for col in range(len(fruit_pos[row])):
				tile_id = fruit_pos[row][col]
				if tile_id == 0:
					continue
				
				fruit = Fruits('Apple')
				
				fruit.rect.x = (col * tile_size) - (fruit.rect.width//4)
				fruit.rect.y = (row * tile_size) - (fruit.rect.height//4)

				self.collectables.add(fruit)
				self.all_sprites.add(fruit)
	
	def getTilePosition(self, tile_id):
		""" Obtiene la posición en la que se encuentra el sprite del terreno.
		"""
		tile_offset_x = tile_offset_y = 0
		match tile_id:
			case 1:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
			case 2:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
			case 3:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 0)
			case 4:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
			case 5:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
			case 6:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 1)
			case 7:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 0)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
			case 8:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 1)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
			case 9:
				tile_offset_x = terrain_pos[0] + (tile_multiplier * 2)
				tile_offset_y = terrain_pos[1] + (tile_multiplier * 2)
			case 10:
				tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 0)
				tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 0)
			case 11:
				tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 1)
				tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 0)
			case 12:
				tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 0)
				tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 1)
			case 13:
				tile_offset_x = terrain_extra_pos[0] + (tile_multiplier * 1)
				tile_offset_y = terrain_extra_pos[1] + (tile_multiplier * 1)
		return tile_offset_x, tile_offset_y
	
	def draw(self, screen):
		""" Dibuja los sprites y el texto en la escena.
		"""
		# Sprites
		screen.fill((0, 0, 0))
		for tile in self.tiles:
			screen.blit(self.background, tile)
		self.platform_list.draw(screen)
		self.all_sprites.draw(screen)

		# Texto
		screenW, screenH = screen.get_size()

		y_offset = (screenH // 2) - 90

			# Crea el efecto de outline del titulo
		text = self.font_outline.render('HARVEST HEIGHTS', True, (0, 0, 0))
		textRect = text.get_rect()
		textRect.topleft = (50, y_offset)
		textRect.centerx = screen.get_rect().centerx + 1
		screen.blit(text, textRect)

		textRect.centerx = screen.get_rect().centerx - 1
		screen.blit(text, textRect)

		textRect.centerx = screen.get_rect().centerx
		textRect.y += 1
		screen.blit(text, textRect)

		textRect.y -= 2
		screen.blit(text, textRect)

			# Escribe el titulo
		text = self.font_title.render('HARVEST HEIGHTS', True, (255, 255, 255))
		textRect = text.get_rect()
		textRect.topleft = (50, y_offset)
		textRect.centerx = screen.get_rect().centerx
		screen.blit(text, textRect)

		y_offset += 200

			# Escribe el resto del texto
		text = self.font.render('Press ENTER to start', True, (255, 255, 255))
		textRect = text.get_rect()
		textRect.topleft = (50, y_offset)
		textRect.centerx = screen.get_rect().centerx
		screen.blit(text, textRect)
	
	def update(self):
		""" Actualiza el estado de los sprites en la escena.
		"""
		self.all_sprites.update()
	
	def clear(self):
		""" Borra todos los elementos de la escena.
		"""
		self.tiles.clear()
		self.platform_list.empty()
		self.all_sprites.empty()