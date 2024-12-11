# pump.py
import RPi.GPIO as GPIO

class Pump:
    def __init__(self, relay_pin):
        """
        Initializes the pump control relay on the specified GPIO pin.
        """
        self.relay_pin = relay_pin
        GPIO.setup(self.relay_pin, GPIO.OUT)
        self.off()  # Start with pump off

    def on(self):
        """
        Turns the pump on by activating the relay.
        """
        GPIO.output(self.relay_pin, GPIO.LOW)
        print("Pump is ON.")

    def off(self):
        """
        Turns the pump off by deactivating the relay.
        """
        GPIO.output(self.relay_pin, GPIO.HIGH)
        print("Pump is OFF.")
