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


# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

    def display(self):
        # Menggambar bola utama
        pygame.draw.circle(screen, self.color, (int(self.posx), int(self.posy)), self.radius)
        # Menambahkan efek binar mata kecil/kilauan di bola agar terlihat hidup dan lucu
        pygame.draw.circle(screen, WHITE, (int(self.posx) - 2, int(self.posy) - 2), 2)

    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed

        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        if self.posy <= 0:
            self.yFac *= -1

        if self.posy >= HEIGHT:
            return True

        return False

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac, self.yFac = random.choice([-1, 1]), -1

    def hit(self):
        self.yFac *= -1

    def getRect(self):
        # Membuat rect imajiner dari lingkaran agar sistem deteksi tabrakan tidak error
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)


# Helper Functions
def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True
    return False


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []
    for i in range(0, WIDTH, blockWidth+horizontalGap):
        for j in range(0, HEIGHT//2, blockHeight+verticalGap):
            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, 
                      random.choice([WHITE, BLUE])))
    return listOfBlocks


def gameOver():
    gameOver = True
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


# Game Manager
def main():
    running = True
    lives = 3
    score = 0

    scoreText = font.render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (40, HEIGHT-20)

    livesText = font.render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (140, HEIGHT-20)

    # Menggunakan warna PINK_LUCU untuk papan pemukul imut Anda
    striker = Striker(WIDTH // 2 - 50, HEIGHT-50, 100, 20, 12, PINK_LUCU)
    strikerXFac = 0

    ball = Ball(WIDTH // 2, HEIGHT-150, 8, 6, WHITE)

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    particles = []

    # Game loop
    while running:
        screen.fill(BLACK)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        scoreText = font.render("Score : " + str(score), True, WHITE)
        livesText = font.render("Lives : " + str(lives), True, WHITE)

        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        if lives <= 0:
            running = gameOver()

            while listOfBlocks:
                listOfBlocks.pop(0)

            lives = 3
            score = 0
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Collision check
        if(collisionChecker(striker.getRect(), ball.getRect())):
            ball.hit()
            
        for block in listOfBlocks:
            if(collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()

                center_x = block.posx + (block.width // 2)
                center_y = block.posy + (block.height // 2)
                for _ in range(15):
                    particles.append(Particle(center_x, center_y, block.color))

                if block.getHealth() <= 0:
                    listOfBlocks.pop(listOfBlocks.index(block))
                    score += 5

        # Update permainan
        striker.update(strikerXFac)
        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            print(lives)

        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)

        # Display seluruh objek game
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        for particle in particles:
            particle.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()