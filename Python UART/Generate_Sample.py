from tensorflow.keras.datasets import mnist
import numpy as np

(train_images, train_labels), _ = mnist.load_data()
image_test = train_images[0]
# We must use the inverted version!!!!!!!!!!!!!!!!!!!!!!!!, the correct version inverts each byte (0x12345678 --> 0x78563412), since 8-bit == 0x00
# found it by printing out using python, and comparing it to the "sampledata.h" that is produced when converting to C
# This file is used to generate Inverted Matrix of the test sample for testing without UART communication


def print_mnist_layout(image):
    for number in range(int(len(image))):
        if number%28 == 0 : print("")
        if image[number] > -128: print("0", end = "")
        else: print("#", end = "")

def print_matrix(image): # 7x28 array specifically
    print("\n\t{\ ", end = "")
    for rows in range(28):
        print(f"\n\t{image[rows*28]& 0xff:#02x}{image[rows*28+1]& 0xff:02x}{image[rows*28+2]& 0xff:02x}{image[rows*28+3]& 0xff:02x}", end = "")
        for columns in range(6):
            print(f",{image[rows*28 + (columns+1)*4] & 0xff:#02x}{image[rows*28 + (columns+1)*4 + 1] & 0xff:02x}{image[rows*28 + (columns+1)*4 + 2] & 0xff:02x}{image[rows*28 + (columns+1)*4 + 3]& 0xff:02x}", end = "")
        print(", \ ", end = "")
    print("\n\t}")

def print_inverted_matrix(image):
    print("\n\t{\ ", end = "")
    for rows in range(28):
        print(f"\n\t{image[rows*28+3]& 0xff:#02x}{image[rows*28+2]& 0xff:02x}{image[rows*28+1]& 0xff:02x}{image[rows*28]& 0xff:02x}", end = "")
        for columns in range(6):
            print(f",{image[rows*28 + (columns+1)*4 + 3] & 0xff:#02x}{image[rows*28 + (columns+1)*4 + 2] & 0xff:02x}{image[rows*28 + (columns+1)*4 + 1] & 0xff:02x}{image[rows*28 + (columns+1)*4]& 0xff:02x}", end = "")
        print(", \ ", end = "")
    print("\n\t};")

image_test = image_test ^ 128
image_test = image_test.flatten()
print_mnist_layout(image_test)
print_inverted_matrix(image_test)
