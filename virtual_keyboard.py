import math
import pygame
import random

# black background
pygame.init()
pygame.key.set_repeat(200,50)
screen = pygame.display.set_mode((1280, 720))

color = (0,0,0)

running=True
clock =pygame.time.Clock()

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            color = ( 
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
            )

              

    screen.fill(color)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

