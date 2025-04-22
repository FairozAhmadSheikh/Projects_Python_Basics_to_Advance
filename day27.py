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