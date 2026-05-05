import math
import pygame

# black background
pygame.init()
screen = pygame.display.set_mode((400, 300))

r,g,b = 0,0,0
selected = "r"

running=True
clock =pygame.time.Clock()

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            key = event.key 

            if key == pygame.K_r:
                selected = "r"
            elif key ==pygame.K_g:
                selected = "g"
            elif key == pygame.K_b:
                selected = "b"

            elif event.key == pygame.K_UP:
                if selected == "r":
                    r = min(255, r + 5)
                elif selected == "g":
                    g = min(255, g +5)
                elif selected == "b":
                    b = min(255, b +5)

            elif event.key == pygame.K_DOWN:
                if selected == "r":
                    r = max(0, r-5)
                elif selected == "g":
                    g=max(0, g - 5)
                elif selected == "b":
                    b = max(0, b - 5)

    background_color = (r,g,b)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

