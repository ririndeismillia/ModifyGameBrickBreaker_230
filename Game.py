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


# Striker class (Papan Pemukul Lucu)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Mengubah visual papan jadi membulat (lucu)
    def display(self):
        # Menggunakan parameter border_radius agar sudut papan menjadi bulat lonjong comel
        pygame.draw.rect(screen, self.color, self.strikerRect, border_radius=12)
        # Menambahkan variasi garis putih kecil di dalam papan agar terlihat berkilau lucu
        kilau_rect = pygame.Rect(self.posx + 10, self.posy + 4, self.width - 20, 4)
        pygame.draw.rect(screen, WHITE, kilau_rect, border_radius=2)

    def update(self, xFac):
        self.posx += self.speed*xFac

        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.strikerRect


# Block Class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    def display(self):
        if self.health > 0:
            # Membuat sudut balok-balok di atas sedikit membulat juga agar serasi
            pygame.draw.rect(screen, self.color, self.blockRect, border_radius=4)

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


