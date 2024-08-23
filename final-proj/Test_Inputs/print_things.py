import numpy as np
from tensorflow.keras.datasets import mnist

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Select an image from the dataset (e.g., the first image in the training set)
image_index = 0
image = x_train[image_index]
label = y_train[image_index]

# Print the label of the selected image
print(f"Label of the selected image: {label}")

# Print the pixel values of the selected image
print("Pixel values of the selected image:")
for row in image:
    print(' '.join(f'{pixel:3}' for pixel in row))