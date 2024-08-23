import serial
import time
import numpy as np
from tensorflow.keras.datasets import mnist
import csv
import torch

# Communication Settings
RX_SIZE = 20 + 2 #2 for time
TEST_SIZE = 10000
TX_SIZE = 1 * 28 * 28
DELAY = 0
NO_OUTPUTS = 10

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

# Load MNIST dataset
_ , (test_images, test_labels) = mnist.load_data()

# Open csv file
csv_file = "output_MNIST_25_10000.csv"
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

#------------------------------ Start of Actual Test ------------------------------#
writer.writerow(["Total number of test: ", TEST_SIZE])

# Actual Communication
for x in range(TEST_SIZE):
    print(f"\n******************** Start of Test {x+1} ********************\n")
    # Sends Image to Board
    image = test_images[x].flatten()
    label = test_labels[x]
    print(f"The Label of this picture is: {label}")
    
    for hexa in range(int(TX_SIZE/4)):
        for byte in range(3, -1, -1):
            byte_to_send = int(image[hexa * 4 + byte] ^ 128)
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
            #print(f"Received byte: {response[0]} as bits: {received_bits}")
        else:
            print("No response received.")

    print("\nTransmission finish, Printing results...........")
    for y in range(NO_OUTPUTS):
        # The first half of the output is digs, latter half is tens
        print(f"Class {y}: \t{output[y]}.{output[y+10]}")
        writer.writerow([str(y) + ": ", str(output[y]) + "." + str(output[y+10])])

    highest_number = 0
    highest_index = 0
    repeat = 0
    for index in range(10):
        number = output[index] + output[index+10]/100.0
        if number > highest_number:
            highest_index = index
            highest_number = number

    for index in range(10):
        number = output[index] + output[index+10]/100.0
        if number == highest_number:
            repeat = repeat + 1
    
    if label != highest_index: writer.writerow(["Wrong"])
    elif repeat > 1: writer.writerow(["Wrong"])
    else: writer.writerow(["Correct"])
    writer.writerow(["Time Taken", str(output[20] * 256 + output[21]) + " us"])
                    
    writer.writerow([])
    print(f"\n******************** End of Test {x+1} ********************\n")
    print("\n-----------------------------------------------------------------------------------------\n")
    
# Ensure the serial port is closed
ser.close()
file.close()
print(f"Closed serial port {serial_port}.")
