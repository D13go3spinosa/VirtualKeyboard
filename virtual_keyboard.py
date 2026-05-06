import sounddevice as sd
import pygame
import random

sample_rate = 44100
active_notes = {}

key_map = {
    pygame.K_a: 261.63,
    pygame.K_s: 293.66,
    pygame.K_d: 329.63,
    pygame.K_f: 349.23,
    pygame.K_g: 392.00,
    pygame.K_h: 440.00,
    pygame.K_j: 493.88,
}

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

