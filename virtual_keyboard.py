import sounddevice as sd
import numpy as np
import pygame
import random
import threading

sample_rate = 44100
active_notes = {}
lock = threading.Lock()

key_map = {
    pygame.K_a: 261.63,
    pygame.K_s: 293.66,
    pygame.K_d: 329.63,
    pygame.K_f: 349.23,
    pygame.K_g: 392.00,
    pygame.K_h: 440.00,
    pygame.K_j: 493.88,
}
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


