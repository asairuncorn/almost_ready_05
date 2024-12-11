import Adafruit_ADS1x15
from time import sleep

class PressureSensor:
    def __init__(self):
        # Gain setting for ADS1115 (2/3 for reading 0 to 6.144V)
        self.GAIN = 2 / 3
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.values = [0, 0]  # Store raw ADC values for both sensors
        self.volts = [0, 0]   # Store voltage readings
        self.psi = [0, 0]     # Store PSI readings for both sensors

    def read_data(self):
        # Read data for sensor 1 (channel 0)
        self.values[0] = self.adc.read_adc(0, gain=self.GAIN)
        self.volts[0] = self.values[0] / 32767.0 * 6.144
        self.psi[0] = 50.0 * self.volts[0] - 25.0

        # Read data for sensor 2 (channel 1)
        self.values[1] = self.adc.read_adc(1, gain=self.GAIN)
        self.volts[1] = self.values[1] / 32767.0 * 6.144
        self.psi[1] = 50.0 * self.volts[1] - 25.0

        print("Sensor 1 - Voltage: {0:0.3f}V, PSI: {1:0.0f}".format(self.volts[0], self.psi[0]))
        print("Sensor 2 - Voltage: {0:0.3f}V, PSI: {1:0.0f}".format(self.volts[1], self.psi[1]))

        return self.psi


sensor = PressureSensor()
while True:
        sensor.read_data()
        sleep(1)
