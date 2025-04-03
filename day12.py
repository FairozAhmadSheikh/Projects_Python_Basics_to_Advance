import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
class SnakeGame:
    def __init__(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = (GRID_SIZE, 0)
        self.food = self.spawn_food()
        self.running = True
        self.score = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if food not in self.snake:
                return food
def move(self):
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in self.snake):
            self.running = False
            return
        
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()
            def draw(self):
                screen.fill(BLACK)
                for segment in self.snake:
                pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, RED, (*self.food, GRID_SIZE, GRID_SIZE))
                pygame.display.flip()
                def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, GRID_SIZE):
                    self.direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and self.direction != (0, -GRID_SIZE):
                    self.direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and self.direction != (GRID_SIZE, 0):
                    self.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-GRID_SIZE, 0):
                    self.direction = (GRID_SIZE, 0)