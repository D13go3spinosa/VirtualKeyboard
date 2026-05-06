import sounddevice as sd
import numpy as np
import pygame
import random
import threading

particles = []
class Particle: 
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.radius = random.randint(2,5)
        self.color=(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        self.vel_x = random.uniform(-3,3)
        self.vel_y = random.uniform(-3,3)
        self.life = random.randint(30,60)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y 
        self.vel_y += 0.05 
        self.life -=1 
    
    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)



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
    t = np.arange(frames) / sample_rate
    signal = np.zeros(frames)

    with lock:
        notes = list(active_notes.values())

    for freq in notes:
       saw = 2*(t * freq - np.floor(0.5 + t * freq))
       
       detune1 = 2 * (t * freq* 1.01 - np.floor(0.5+ t * freq * 1.01))
       detune2 = 2 * (t * freq* 0.99 - np.floor(0.5+ t * freq * 0.99))

       voice = saw + 0.5 * detune1 + 0.5 * detune2

       envelope = np.linspace(1,0.2,frames)

       signal += voice * envelope 

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
            if event.key in key_map:
                with lock:
                    active_notes[event.key] = key_map[event.key]
            
            x = random.randint(100,1180)
            y= random.randint(100, 620)
            
            for _ in range(30):
                particles.append(Particle(x,y))

            
    screen.fill((10,10,20))
    for particle in particles [:]:
        particle.update()
        particle.draw(screen)

        if particle.life <=0:
            particles.remove(particle)
    pygame.display.flip()
    clock.tick(60)
stream.stop()    
pygame.quit()


