import numpy as np
import matplotlib.pyplot as plt

# Generate the pattern using parametric equations
t = np.linspace(0, 10 * np.pi, 1000)
x = np.sin(3 * t) * np.cos(2 * t)
y = np.sin(2 * t) * np.cos(3 * t)

# Create the plot
plt.figure(figsize=(6,6), facecolor='black')
plt.plot(x, y, color='cyan', linewidth=2)
plt.axis('off')  # Hide axes

# Display the art
plt.show()
