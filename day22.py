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

# Loss
def cross_entropy(pred, true):
    return -np.sum(true * np.log(pred + 1e-9)) / pred.shape[0]

# Training
def train(epochs=1000, lr=0.1):
    global W1, b1, W2, b2
    for epoch in range(epochs):
        # Forward
        z1 = X_train @ W1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ W2 + b2
        a2 = softmax(z2)

        # Loss
        loss = cross_entropy(a2, y_train)

        # Backprop
        dz2 = a2 - y_train
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = dz2 @ W2.T
        dz1 = da1 * a1 * (1 - a1)
        dW1 = X_train.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Update weights
        W2 -= lr * dW2
        b2 -= lr * db2
        W1 -= lr * dW1
        b1 -= lr * db1

        if epoch % 100 == 0:
            print(f"Epoch {epoch} | Loss: {loss:.4f}")