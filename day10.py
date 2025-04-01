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
def train_neural_network(X, y, epochs=10000, learning_rate=0.1):
    """Trains a simple 2-layer neural network on the XOR dataset."""
    np.random.seed(42)
    input_size = 2
    hidden_size = 4
    output_size = 1
     # Initialize weights
    weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
    weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))
    
    for epoch in range(epochs):
        # Forward pass
        hidden_layer_input = np.dot(X, weights_input_hidden)
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
        output = sigmoid(output_layer_input)
        # Compute error
        error = y - output
        # Backpropagation
        d_output = error * sigmoid_derivative(output)
        d_hidden = d_output.dot(weights_hidden_output.T) * sigmoid_derivative(hidden_layer_output)
              # Update weights
        weights_hidden_output += hidden_layer_output.T.dot(d_output) * learning_rate
        weights_input_hidden += X.T.dot(d_hidden) * learning_rate
        
        if epoch % 1000 == 0:
            loss = np.mean(np.abs(error))
            print(f"Epoch {epoch}, Loss: {loss}")
        return weights_input_hidden, weights_hidden_output

def predict(X, weights_input_hidden, weights_hidden_output):
    """Makes predictions using the trained neural network."""
    hidden_layer_input = np.dot(X, weights_input_hidden)
    hidden_layer_output = sigmoid(hidden_layer_input)
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
    return sigmoid(output_layer_input)
def main():
    print("Training XOR Neural Network...")
    X, y = generate_dataset(1000)
    weights_input_hidden, weights_hidden_output = train_neural_network(X, y)