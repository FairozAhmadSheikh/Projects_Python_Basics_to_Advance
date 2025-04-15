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
# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

# Initialize weights
input_size = 64      # 8x8 images
hidden_size = 32
output_size = 10     # digits 0-9