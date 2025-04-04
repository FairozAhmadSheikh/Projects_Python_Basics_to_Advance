import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load assets
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 5
        self.bullets = []

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(WIDTH - 64, self.x))

    def shoot(self):
        self.bullets.append(Bullet(self.x + 16, self.y))

    def draw(self):
        screen.blit(player_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()
# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 64)
        self.y = random.randint(50, 150)
        self.speed = 3
        self.direction = 1

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WIDTH - 64:
            self.direction *= -1
            self.y += 40

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -7
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y < 0:
            self.active = False

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))
# Collision detection
def is_collision(obj1, obj2):
    distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
    return distance < 30

def main():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    score = 0

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies:
            enemy.move()
            enemy.draw()
        
        for bullet in player.bullets:
            bullet.move()
            if not bullet.active:
                player.bullets.remove(bullet)
        
        for enemy in enemies[:]:
            for bullet in player.bullets[:]:
                if is_collision(enemy, bullet):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    score += 1
                    break
        
        player.draw()
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
