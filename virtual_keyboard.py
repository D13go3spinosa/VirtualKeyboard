import math
import pygame

# black background
pygame.init()
screen = pygame.display.set_mode((400, 300))
background_color = (0,0,0)

running=True
while running: 
    for event in pygame.event.get():
        running= False 
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            background_color = (255,0,0) #RED
        if event.key == pygame.K_2:
            background_color = (0,255,0)

    screen.fill(background_color)
    pygame.display.flip()

    pygame.quit()

