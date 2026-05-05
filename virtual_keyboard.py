import math
import pygame

# black background
pygame.init()
pygame.key.set_repeat(200,50)
screen = pygame.display.set_mode((400, 300))

color = (0,0,0)

running=True
clock =pygame.time.Clock()

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    color = (255,0,0)
                elif event.key == pygame.K_2:
                    color = (0,255,0)
                elif event.key == pygame.K_3:
                    color = (0,0,255)
                elif event.key == pygame.K_4:
                    color = (255, 255, 0)
                elif event.key == pygame.K_5:
                    color = (255,255,255)

              

    screen.fill(color)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

