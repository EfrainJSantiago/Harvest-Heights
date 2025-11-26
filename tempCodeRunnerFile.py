start_screen = Start(screen)

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

	screen.fill((0, 0, 0))
	start_screen.draw(screen)

	mainClock.tick(60)
	pygame.display.flip()

start_screen.clear()