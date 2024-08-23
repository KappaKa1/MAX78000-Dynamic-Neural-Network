#***********************************************************************************************************
# The code below communicates the MNIST dataset using an UART cable which is connected to a external device*
# by KAI CHENG                                                                                             *
#***********************************************************************************************************

import serial
import numpy as np
from tensorflow.keras.datasets import mnist
import csv
import time

START_BIT = 0;
END_BIT = 1;

TEST_SIZE = 1
NUM_OF_OUTPUTS = 10
DIMENSION = [1, 28, 28]
BYTE_SIZE = 8

# Load MNIST dataset
(train_images, train_labels), _ = mnist.load_data()

# Open csv file
csv_file = "output.csv"


# Initialize serial port
ser = serial.Serial(
    port = 'COM9',        # Replace with your port name (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows)
    baudrate = 115200,      # Set the baud rate to match your UART device
    timeout = 1,          # Set a timeout for reading (in seconds)
)


def receive_uart_data(ser):
    ser.setRTS(True)
    print("Receiver is ready.")
    
    while true:
        if ser.in_waiting > 0:  # Check if there is data in the buffer
            data = ser.read(1)  # Read 1 byte from the buffer
            bits = format(ord(data), '08b')  # Convert byte to bits (8-bit binary string)
            print(f"Received byte: {data}, Bits: {bits}")
            return bits
        time.sleep(0.1)


def transmit_uart_data(ser, bits):
    # Convert bits (binary string) to a byte
    byte_data = bytes([int(bits, 2)])
        
    ser.write(byte_data)  # Transmit the byte
    print(f"Transmitted Bits: {bits}, Byte: {byte_data}")


# Convert the image to a binary string
def image_to_bits(image):
    bits = ''.join(format(pixel, '08b') for row in image for pixel in row)
    return bits


file = open(csv_file, mode='w', newline='')
writer = csv.writer(file)
no_loops = (DIMENSION[0] * DIMENSION[1] * DIMENSION[2]) * BYTE_SIZE #Due to the conversion from np.int8 to np.int64

for x in range(TEST_SIZE):
    # Assigning respective MNIST dataset
    image = train_images[0]
    label = train_labels[0]
    writer.writerow(["The Label of this picture is:", label])
        
    # Preparing Data for communication 
    image = image.astype(np.int64) # Converting Data to type np.int64
    bits = image_to_bits(image)
              
    # Transmit data
    for y in range(196):
        start_index = y * BYTE_SIZE
        end_index = start_index + BYTE_SIZE
        transmit_uart_data(ser, bits[start_index:end_index])
                
    # Receive data
    #for z in range(NUM_OF_OUTPUTS):
    #    digs = receive_uart_data(ser)
    #    tens = receive_uart_data(ser)
    #    perc1 = int(digs, 2)
    #    perc2 = int(tens, 2)
    #    writer.writerow([str(z) + ":", str(perc1) + "." + str(perc2)])
    #writer.writerow([""])

file.close() # Clost CSV file
ser.close()  # Close the serial port when done