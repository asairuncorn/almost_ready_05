import RPi.GPIO as GPIO
import time

# Pin configuration
DATA_PIN = 17   # SER (DS)
CLOCK_PIN = 27  # SRCLK
LATCH_PIN = 22  # RCLK
INPUT_PIN = 5   # GPIO pin to read switches
NUM_SWITCHES = 4

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to send data to 74HC595
def shift_out(data):
    GPIO.output(LATCH_PIN, 0)  # Begin latch operation
    for bit in range(8):  # Send 8 bits
        GPIO.output(CLOCK_PIN, 0)  # Set clock to LOW
        GPIO.output(DATA_PIN, (data >> (7 - bit)) & 1)  # Write MSB first
        GPIO.output(CLOCK_PIN, 1)  # Set clock to HIGH
    GPIO.output(LATCH_PIN, 1)  # Finalize latch

# Read switches
def read_switches():
    states = []
    for i in range(NUM_SWITCHES):
        # Activate one output at a time
        shift_out(1 << i)  # Set Q(i) HIGH, others LOW
        time.sleep(0.01)  # Short delay to stabilize signals
        states.append(GPIO.input(INPUT_PIN))  # Read input pin
    return states

# Main loop
try:
    while True:
        switch_states = read_switches()
        for i, state in enumerate(switch_states):
            print(f"Switch {i + 1}: {'ON' if state else 'OFF'}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting program...")
finally:
    GPIO.cleanup()
