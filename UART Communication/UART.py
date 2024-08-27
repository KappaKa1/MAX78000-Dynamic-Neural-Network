import pickle
import serial
import time
import numpy as np
from tensorflow.keras.datasets import mnist
import csv
import torch
import os

# Communication Settings
RX_SIZE = 200 + 2 #2 for time
TEST_SIZE = 10000
TX_SIZE = 3 * 32 * 32
DELAY = 0
NO_OUTPUTS = 100

# UART Settings
BAUD_RATE = 115200
PORT = 'COM9'
TIMEOUT = 2

# Variables
output = np.zeros(RX_SIZE, dtype=np.uint8)

# Configure the serial port
serial_port = PORT  # Replace with your serial port (e.g., '/dev/ttyUSB0' on Linux/macOS)
baud_rate = BAUD_RATE      # Replace with your baud rate
timeout = TIMEOUT           # 1-second timeout for read operations

# Load CIFAR100 dataset and normalize
def load_file(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

cifar100_dir = 'data/cifar-100-python'  # Replace with the correct path
train_file = os.path.join(cifar100_dir, 'train')
test_file = os.path.join(cifar100_dir, 'test')
meta_file = os.path.join(cifar100_dir, 'meta')

train_data = load_file(train_file)
test_data = load_file(test_file)
meta_data = load_file(meta_file)

train_images = train_data[b'data']
train_labels = train_data[b'fine_labels']
test_images = test_data[b'data']
test_labels = test_data[b'fine_labels']
classes = [label.decode('utf-8') for label in meta_data[b'fine_label_names']]

train_images = train_images.reshape(-1, 3, 32, 32) ^ 128
test_images = test_images.reshape(-1, 3, 32, 32) ^ 128

# Open csv file
csv_file = "output_CIFAR100_simplewide2x.csv"
file = open(csv_file, mode='w', newline='')
writer = csv.writer(file)

# Open the serial connection
ser = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=timeout)
print(f"Opened serial port {serial_port} at {baud_rate} baud.")

# Give the connection a second to settle
time.sleep(2)

# Waits for the board to send the "Start" Signal
times = 0;
while times < RX_SIZE:
    response = ser.read(1)  # Read 1 byte from the board
    if response:
        received_bits = bin(int.from_bytes(response, 'big'))[2:].zfill(8)  # Convert to binary and pad to 8 bits
        print(f"Received byte: {response[0]} as bits: {received_bits}")
        times = 1 + times
    else:
        print("No response received.")


writer.writerow(["Total number of test: ", TEST_SIZE])

# Actual Communication
for x in range(TEST_SIZE):
    print(f"\n******************** Start of Test {x+1} ********************\n")
    # Sends Image to Board
    image = test_images[x]
    label = test_labels[x]
    print(f"The Label of this picture is: {label}")
    
    for column in range(32):
        for row in range(32):
            for layers in range(3, -1, -1):
                if layers == 3: byte_to_send = 0
                else: byte_to_send = int(image[layers][column][row])
                byte_data = byte_to_send.to_bytes(1, byteorder='big', signed=False)
                ser.write(byte_data)

    writer.writerow(["This is test number: ", x])
    writer.writerow(["The Label of this picture is: ", label])
    time.sleep(DELAY)

    times = 0
    # Receives Output from Board    
    while times < RX_SIZE:
        response = ser.read(1)  # Read 1 byte from the board
        if response:
            received_bits = bin(int.from_bytes(response, 'big'))[2:].zfill(8)  # Convert to binary and pad to 8 bits
            output[times] = response[0]
            times = 1 + times
        else:
            print("No response received.")

    print("\nTransmission finish, Printing results...........")
    for y in range(NO_OUTPUTS):
        # The first half of the output is digs, latter half is tens
        print(f"Class {y}: \t{output[y]}.{output[y + NO_OUTPUTS]}")
        writer.writerow([str(int(y)) + ": ", str(output[y]) + "." + str(output[y + NO_OUTPUTS])])

    highest_number = 0
    highest_index = 0
    repeat = 0
    correct_repeat = False
    for index in range(NO_OUTPUTS):
        number = output[index] + output[index + NO_OUTPUTS]/100.0
        if number > highest_number:
            highest_index = index
            highest_number = number

    for index in range(NO_OUTPUTS):
        number = output[index] + output[index + NO_OUTPUTS]/100.0
        if number == highest_number:
            if label == index: correct_repeat = True
            repeat = repeat + 1
    
    if correct_repeat and repeat == 1: writer.writerow(["Correct"])
    elif correct_repeat and repeat <= 5: writer.writerow(["TOP 5"])
    else: writer.writerow(["Wrong"])
    
    writer.writerow(["Time Taken", str(output[RX_SIZE - 2] * 256 + output[RX_SIZE - 1]) + " us"])
                    
    writer.writerow([])
    print(f"\n******************** End of Test {x+1} ********************\n")
    print("\n-----------------------------------------------------------------------------------------\n")
    
# Ensure the serial port is closed
ser.close()
file.close()
print(f"Closed serial port {serial_port}.")
