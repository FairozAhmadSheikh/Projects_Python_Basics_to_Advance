import numpy as np
import cv2
import random
import time

def generate_maze(size=20):
    """Generates a random maze using recursive division."""
    maze = np.ones((size, size), dtype=np.uint8) * 255
    def divide(x, y, width, height):
        if width < 3 or height < 3:
            return
        
        horizontal = width < height
        if horizontal:
            wx = x
            wy = y + random.randint(1, height - 2)
            px = wx + random.randint(0, width - 1)
            for i in range(x, x + width):
                if i != px:
                    maze[wy, i] = 0
            divide(x, y, width, wy - y)
            divide(x, wy + 1, width, y + height - wy - 1)
        else:
            wx = x + random.randint(1, width - 2)
            wy = y
            py = wy + random.randint(0, height - 1)
            for i in range(y, y + height):
                if i != py:
                    maze[i, wx] = 0
            divide(x, y, wx - x, height)
            divide(wx + 1, y, x + width - wx - 1, height)
        divide(0, 0, size, size)
        maze[1, 0] = maze[size - 2, size - 1] = 255  # Entrance and exit
        return maze
def solve_maze(maze):
    """Solves the maze using A* algorithm."""
    size = maze.shape[0]
    start, end = (1, 0), (size - 2, size - 1)
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(end[0] - start[0]) + abs(end[1] - start[1])}
def neighbors(pos):
    x, y = pos
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size and maze[nx, ny] == 255:
            yield (nx, ny)
    while open_set:
current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
if current == end:
path = []
while current in came_from:
    path.append(current)
    current = came_from[current]
    path.append(start)
        return path[::-1]

open_set.remove(current)
for neighbor in neighbors(current):
temp_g_score = g_score[current] + 1
if temp_g_score < g_score.get(neighbor, float('inf')):
    came_from[neighbor] = current
    g_score[neighbor] = temp_g_score
    f_score[neighbor] = temp_g_score + abs(end[0] - neighbor[0]) + abs(end[1] - neighbor[1])
    open_set.add(neighbor)
return []
def display_maze(maze, path=[]):
    """Displays the maze and solution using OpenCV."""
    size = maze.shape[0] * 10
    img = cv2.resize(maze, (size, size), interpolation=cv2.INTER_NEAREST)
    for (x, y) in path:
        cv2.circle(img, (y * 10 + 5, x * 10 + 5), 3, (0, 0, 255), -1)
    cv2.imshow("Maze", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()