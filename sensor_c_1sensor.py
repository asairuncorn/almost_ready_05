from time import sleep
import Adafruit_ADS1x15

class PressureSensor:
    def __init__(self):
        # Gain setting for ADS1115 (2/3 for reading 0 to 6.144V)
        self.GAIN = 2 / 3
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.values1 = 0  # Raw ADC value for sensor 1
        self.volts1 = 0   # Voltage reading for sensor 1
        self.psi1 = 0     # PSI reading for sensor 1
        self.values2 = 0  # Raw ADC value for sensor 2
        self.volts2 = 0   # Voltage reading for sensor 2
        self.psi2 = 0     # PSI reading for sensor 2

    def read_data(self):
        # Read data for sensor 1 (channel 0)
        self.values1 = self.adc.read_adc(0, gain=self.GAIN)
        self.volts1 = self.values1 / 32767.0 * 6.144
        self.psi1 = 50.0 * self.volts1 - 25.0

        # Add a delay to ensure stable reading when switching channels
        sleep(0.1)

        # Read data for sensor 2 (channel 1)
        self.values2 = self.adc.read_adc(1, gain=self.GAIN)
        self.volts2 = self.values2 / 32767.0 * 6.144
        self.psi2 = 50.0 * self.volts2 - 25.0

        # Print readings with consistent labeling
        print("Sensor 1 - Voltage: {0:0.3f}V, PSI: {1:0.0f}".format(self.volts1, self.psi1))
        print("Sensor 2 - Voltage: {0:0.3f}V, PSI: {1:0.0f}".format(self.volts2, self.psi2))

        # Return both PSI readings
        return self.psi1, self.psi2
