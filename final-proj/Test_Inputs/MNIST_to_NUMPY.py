import numpy as np
from tensorflow.keras.datasets import mnist

SIZE = 10000

# Load MNIST dataset
(train_images, train_labels), _ = mnist.load_data()

# Select the first 10,000 samples
train_images = train_images[:SIZE]
train_labels = train_labels[:SIZE]

# Convert each element to np.int64
train_images = train_images.astype(np.int64)
train_labels = train_labels.astype(np.int64)

# Save the arrays to a .np file
np.savez('mnist_10000_int64.npz', images=train_images, labels=train_labels)

# Confirm the file was saved
print('Data saved to mnist_10000_int64.npz')