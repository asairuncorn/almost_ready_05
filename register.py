# Raspberry Pi and 74HC595 Shift Register

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep

GPIO.setwarnings(False)  # Ignore warning for now

GPIO.setmode(GPIO.BCM)  # Use chip GPIO numbering

SDI = 17  # Pin 11
SRCLK = 27  # Pin 13
RCLK = 22  # Pin 15

GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)  # Set pin 11 to be an output pin and set initial value to low
GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)  # Set pin 13 to be an output pin and set initial value to low
GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)  # Set pin 15 to be an output pin and set initial value to low

BitPattern = [0x18, 0x24, 0x42, 0x81]


def Send_Data_74HC595(value):
    # --------Shift out 8 bits-----------------------
    for bit in range(0, 8):
        GPIO.output(SDI, 0x80 & (value << bit))
        GPIO.output(SRCLK, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
    # -------Transfer shifted bits to output---------
    GPIO.output(RCLK, GPIO.HIGH)
    sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    # -----------------------------------------------


while True:
    Send_Data_74HC595(BitPattern[0])
    sleep(0.2)
    Send_Data_74HC595(BitPattern[1])
    sleep(0.2)
    Send_Data_74HC595(BitPattern[2])
    sleep(0.2)
    Send_Data_74HC595(BitPattern[3])
    sleep(0.2)

