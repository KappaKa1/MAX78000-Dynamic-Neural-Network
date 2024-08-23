import serial
import time
import numpy as np
from tensorflow.keras.datasets import mnist
import csv

# Constant Variables
BYTE_SIZE = 8
Rx_Size = 20
Test_Size = 20;
Tx_Size = 28 * 28

def image_to_bits(image):
    bits = ''.join(format(pixel, '08b') for row in image for pixel in row)
    return bits

# Configure the serial port
serial_port = 'COM9'  # Replace with your serial port (e.g., '/dev/ttyUSB0' on Linux/macOS)
baud_rate = 115200      # Replace with your baud rate
timeout = 1           # 1-second timeout for read operations

# Load MNIST dataset
(train_images, train_labels), _ = mnist.load_data()

# Open csv file
#csv_file = "output.csv"


    # Open the serial connection
ser = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=timeout)
print(f"Opened serial port {serial_port} at {baud_rate} baud.")

    # Give the connection a second to settle
time.sleep(2)


# Waits for the board to send the "Start" Signal
times = 0;
while times < Rx_Size:
    response = ser.read(1)  # Read 1 byte from the board
    if response:
        received_bits = bin(int.from_bytes(response, 'big'))[2:].zfill(8)  # Convert to binary and pad to 8 bits
        print(f"Received byte: {response[0]} as bits: {received_bits}")
        times = 1 + times
    else:
        print("No response received.")

for x in range(Test_Size):
    print(f"This is the {x+1} times")
    # Sends Image to Board
    image = train_images[x]
    label = train_labels[x]
    #writer.writerow(["The Label of this picture is:", label])
    image = image.astype(np.int64) # Converting Data to type np.int64
    bits = image_to_bits(image)
   
    for y in range(Tx_Size):
        start_index = y * BYTE_SIZE
        end_index = start_index + BYTE_SIZE
        byte_to_send = int(bits[start_index:end_index], 2)
        ser.write(bytes([byte_to_send]))
        print(f"{y}: Sent bits: {bits[start_index:end_index]} as byte: {byte_to_send}")

    time.sleep(2)

    times = 0
    # Receives Output from Board    
    while times < Rx_Size:
        response = ser.read(1)  # Read 1 byte from the board
        if response:
            received_bits = bin(int.from_bytes(response, 'big'))[2:].zfill(8)  # Convert to binary and pad to 8 bits
            print(f"Received byte: {response[0]} as bits: {received_bits}")
            times = 1 + times
        else:
            print("No response received.")

# Ensure the serial port is closed
ser.close()
print(f"Closed serial port {serial_port}.")
