import sounddevice as sd
import numpy as np
import pygame
import random
import threading

sample_rate = 44100
active_notes = {}
lock = threading.Lock()

keys = [
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b,
    pygame.K_n, pygame.K_m,
    pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, 

    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, 
    pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l,

    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, 
    pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p
]
base_freq = 261.63

key_map = {}
for i, key in enumerate(keys):
    freq = base_freq * (2 **(i / 12))
    key_map[key] = freq

def audio_callback(outdata, frames, time, status):
    time = np.arange(frames) / sample_rate
    signal = np.zeros(frames)

    with lock:
        notes = list(active_notes.values())

    for freq in notes:
        signal += np.sin(2 * np.pi * freq * time)

    if notes:
        signal /= len(notes)

    outdata[:] = signal.reshape(-1,1)

stream = sd.OutputStream(
        channels=1,
        callback= audio_callback,
        samplerate=sample_rate,
        )
stream.start()




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

            if event.key in key_map:
                with lock:
                    active_notes[event.key] = key_map[event.key]

        elif event.type == pygame.KEYUP:
            with lock:
                if event.key in active_notes:
                    del active_notes[event.key]
        

              

    screen.fill(color)
    pygame.display.flip()
    clock.tick(60)
stream.stop()    
pygame.quit()


