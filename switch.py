# switch.py
import RPi.GPIO as GPIO

class Switch:
    def __init__(self, pin):
        """
        Initializes the switch on the specified GPIO pin.
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        """
        Checks if the switch is pressed (high signal).
        """

        return GPIO.input(self.pin) == GPIO.HIGH
