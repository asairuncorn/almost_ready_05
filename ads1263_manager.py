import time
import threading
import ADS1263
import RPi.GPIO as GPIO


class ADS1263Manager:
    def __init__(self, channels, ref_voltage=5.08, sampling_rate='ADS1263_10SPS'):
        """
        Initializes the ADS1263Manager.

        :param channels: List of ADC channels to read from.
        :param ref_voltage: Reference voltage for ADC calculations.
        :param sampling_rate: Sampling rate for ADC initialization.
        """
        self.channels = channels
        self.ref_voltage = ref_voltage
        self.sampling_rate = sampling_rate
        self.ADC = ADS1263.ADS1263()
        self.running = False
        self.data_lock = threading.Lock()
        self.data = {channel: 0 for channel in channels}
        self.thread = threading.Thread(target=self._run, daemon=True)

        # Initialize ADC
        if self.ADC.ADS1263_init_ADC1(self.sampling_rate) == -1:
            raise RuntimeError("Failed to initialize ADS1263")

        self.ADC.ADS1263_SetMode(0)  # Set to single-channel mode

    def start(self):
        """
        Starts the ADC manager thread.
        """
        if not self.running:
            self.running = True
            self.thread.start()

    def stop(self):
        """
        Stops the ADC manager thread.
        """
        self.running = False
        self.thread.join()

    def get_data(self):
        """
        Retrieves the latest ADC data.

        :return: A dictionary containing channel data.
        """
        with self.data_lock:
            return self.data.copy()

    def _run(self):
        """
        Background thread to continuously read ADC data.
        """
        while self.running:
            try:
                adc_values = self.ADC.ADS1263_GetAll(self.channels)
                with self.data_lock:
                    for i, channel in enumerate(self.channels):
                        if adc_values[i] >> 31 == 1:
                            self.data[channel] = -(self.ref_voltage * 2 - adc_values[i] * self.ref_voltage / 0x80000000)
                        else:
                            self.data[channel] = adc_values[i] * self.ref_voltage / 0x7fffffff

                time.sleep(0.1)  # Adjust sampling interval as needed

            except Exception as e:
                print(f"Error in ADS1263Manager: {e}")
                self.running = False

        # Cleanup on stop
        self.ADC.ADS1263_Exit()


# # Usage in your main program
# if __name__ == "__main__":
#     ads_manager = ADS1263Manager(channels=[0, 1])
#     ads_manager.start()
#
#     try:
#         while True:
#             adc_data = ads_manager.get_data()
#             print("ADC Data:", adc_data)
#             time.sleep(1)
#
#     except KeyboardInterrupt:
#         print("Stopping ADS1263Manager...")
#         ads_manager.stop()