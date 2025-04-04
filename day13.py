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