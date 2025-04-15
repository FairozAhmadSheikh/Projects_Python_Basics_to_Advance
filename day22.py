import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load data
digits = load_digits()
X = digits.data / 16.0  # Normalize
y = digits.target.reshape(-1, 1)

# One-hot encode targets
encoder = OneHotEncoder(sparse=False)
y_encoded = encoder.fit_transform(y)