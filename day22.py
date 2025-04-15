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
np.random.seed(42)
W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# Activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)
