# led.py
import RPi.GPIO as GPIO


class LED:
    def __init__(self, pin):
        """
        Initializes the LED on the specified GPIO pin.
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()  # Start with LED off

    def set_green(self):
        """
        Turns the LED green to indicate the pump is on.
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def set_yellow(self):
        """
        Turns the LED yellow to indicate the pump is off.
        """
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        """
        Turns off the LED.
        """
        GPIO.output(self.pin, GPIO.LOW)
