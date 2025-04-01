import numpy as np
import random
import time
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def generate_dataset(samples=1000):
    """Generates a dataset for XOR operation."""
    X = np.random.randint(0, 2, (samples, 2))
    y = np.array([a ^ b for a, b in X])
    return X, y.reshape(-1, 1)
