import pygame
import random

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)      # Biru cerah yang lebih lembut
PINK_LUCU = (255, 105, 180) # Warna merah muda lucu untuk variasi papan
RED = (255, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Cute Edition")

# to control the frame rate
clock = pygame.time.Clock()
FPS = 30


# --- CLASS PARTIKEL (EFEK PECAHAN) ---
class Particle:
    def __init__(self, posx, posy, color):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.radius = random.randint(2, 5)
        self.x_speed = random.uniform(-4, 4)
        self.y_speed = random.uniform(-4, 4)
        self.lifetime = random.randint(10, 20)

    def update(self):
        self.posx += self.x_speed
        self.posy += self.y_speed
        self.lifetime -= 1

    def display(self):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.posx), int(self.posy)), self.radius)


