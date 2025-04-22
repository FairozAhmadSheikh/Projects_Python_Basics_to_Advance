# pip install numpy
import numpy as np
import tkinter as tk
from tkinter import messagebox
import random

# --- Sudoku Solver ---
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    r, c = 3 * (row // 3), 3 * (col // 3)
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if board[i][j] == num:
                return False
    return True
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# --- Sudoku Generator ---
def fill_grid(grid):
    nums = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                random.shuffle(nums)
                for num in nums:
                    if is_valid(grid, i, j, num):
                        grid[i][j] = num
                        if fill_grid(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

def generate_puzzle():
    grid = np.zeros((9, 9), dtype=int)
    fill_grid(grid)
    # Remove numbers to make it a puzzle
    attempts = 40
    while attempts > 0:
        row, col = random.randint(0,8), random.randint(0,8)
        while grid[row][col] == 0:
            row, col = random.randint(0,8), random.randint(0,8)
        backup = grid[row][col]
        grid[row][col] = 0
        copy = grid.copy()
        if not solve_sudoku(copy):
            grid[row][col] = backup
        attempts -= 1
    return grid
