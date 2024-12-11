import time
import RPi.GPIO as GPIO



class PiPumpController:
    def __init__(self,switch, led, pump, timer ):
        """
        Initializes the PiPumpController with all components.
        """
        self.switch = switch
        self.led = led
        self.pump = pump
        self.timer = timer
        self.pump_active = False


    def check_and_run(self):
        """
        Checks the switch and controls the pump, LED, and timer accordingly.
        """
        if self.switch.is_pressed():
            if not self.pump_active:
                print("Switch pressed. Activating pump.")
                self.start_pump()
        # else:
        #     if self.pump_active:
        #         print("Switch released. Deactivating pump.")
        #         self.stop_pump()
        #     else:
        #         # Emit:   "Install cartridge" status when switch is not pressed
        #         self.socketio.emit('switch_status', {'status': 'install_cartridge'})
        #         print("Switch not pressed. Install cartridge.")

    def start_pump(self):
        """
        Starts the pump, LED, and timer.
        """
        self.pump.on()
        self.led.set_green()
        self.pump_active = True
        self.timer.start()
        self.stop_pump()  # Automatically stop after timer ends

    def stop_pump(self):
        """
        Stops the pump and sets LED to yellow.
        """
        self.pump.off()
        self.led.set_yellow()
        self.pump_active = False

    def run(self):
        """
        Continuously checks the switch state to control the pump and LED.
        """
        print("Starting PiPumpController. Press Ctrl+C to exit.")
        try:
            while True:
                self.check_and_run()
                time.sleep(0.1)  # Delay to avoid excessive CPU usage
        except KeyboardInterrupt:
            print("\nExiting program.")
        finally:
            GPIO.cleanup()

