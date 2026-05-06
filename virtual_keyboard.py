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
    freq = base_freq * (2 **((i-12) / 12))
    key_map[key] = freq

def low_pass(signal, alpha=0.12, resonance = 0.2):
    filtered = np.zeros_like(signal)
    filtered[0] = signal [0]
                          
    for i in range (1, len(signal)):
        filtered[i] = (
            alpha * signal[i] + (1-alpha) * filtered[i-1]
            + resonance * (signal[i]- filtered[i-1])
            )
        
    return filtered 




def audio_callback(outdata, frames, time_info, status):
    t = np.arange(frames) / sample_rate
    signal = np.zeros(frames)
    
    
    with lock:
        notes = list(active_notes.values())
    
    attack = np.minimum(t * 10,1.0)
    decay = np.exp(-t * 3)
    envelope = attack * decay

    drift_lfo = np.sin(2* np.pi * 0.4 * t) * 0.003
    

    for freq in notes:
       
       f = freq * (1 +drift_lfo)
       
       saw = 2*(t * f - np.floor(0.5 + t * f))
       
       detune1 = 2 * (t * f* 1.01 - np.floor(0.5 + t * f * 1.01))
       detune2 = 2 * (t * f* 0.99 - np.floor(0.5 + t * f * 0.99))

       voice = (saw + 0.5 * detune1 + 0.5 * detune2)/2
       
       signal += voice * envelope
    
    
    if notes:
        signal /= len(notes)

    signal = low_pass(signal, alpha= 0.12)

    stereo = np.zeros((frames, 2))
    stereo[:, 0] = signal
    stereo[:, 1] = signal * 0.98

    outdata[:] = stereo

stream = sd.OutputStream(
        channels=2,
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
            
            note_count = len(active_notes)
            
            for _ in range(20 + note_count * 5):
                particles.append(Particle(x,y))

        elif event.type == pygame.KEYUP:
            with lock:
                if event.key in active_notes:
                    del active_notes[event.key]

            
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


