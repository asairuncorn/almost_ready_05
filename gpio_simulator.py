# gpio_simulator.py

class GPIO:
    BCM = "BCM"
    IN = "IN"
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"
    PUD_DOWN = "PULL_DOWN"

    pins = {}

    @staticmethod
    def setmode(mode):
        print(f"GPIO Mode set to {mode}")

    @staticmethod
    def setup(pin, mode, pull_up_down=None):
        GPIO.pins[pin] = {"mode": mode, "state": GPIO.LOW}
        print(f"Pin {pin} set up as {mode} with pull-up/down {pull_up_down}")

    @staticmethod
    def input(pin):
        state = GPIO.pins.get(pin, {}).get("state", GPIO.LOW)
        print(f"Read from pin {pin}: {state}")
        return state == GPIO.HIGH

    @staticmethod
    def output(pin, state):
        GPIO.pins[pin]["state"] = state
        state_str = "HIGH" if state == GPIO.HIGH else "LOW"
        print(f"Set pin {pin} to {state_str}")

    @staticmethod
    def cleanup():
        print("Cleaning up GPIO")
        GPIO.pins.clear()

    @staticmethod
    def set_pin_state(pin, state):
        """Helper method to manually set the state of a pin."""
        if pin in GPIO.pins:
            GPIO.pins[pin]["state"] = state
            print(f"Manually set pin {pin} to {state}")
        else:
            print(f"Pin {pin} is not set up.")
