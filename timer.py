
import time

# from pip._vendor.rich import progress
#
# from sensor import*

class Timer:
    def __init__(self, duration, pressure_sensor, ):
        """
        Initializes the timer with a specified duration in seconds.
        """

        self.duration = duration
        self.remaining_time = duration
        self.pressure_sensor = pressure_sensor


    def start(self, callback):
        """
        Starts the countdown timer and displays the remaining time.
        """


        start_time = time.time()
        while self.remaining_time > 0:  # Loop until the remaining time reaches 0

            elapsed_time = time.time() - start_time  # Calculate elapsed time
            self.remaining_time = max(0, self.duration - int(elapsed_time))  # Update remaining time
            percentage_pass = ((self.duration - self.remaining_time) / self.duration) * 100  # Calculate percentage passed

            print(f"Time remaining: {self.remaining_time} seconds", end='\r')
            callback(int(percentage_pass))  # Pass percentage to callback

            time.sleep(1)  # Wait for 1 second

        # Ensure the callback is triggered with 100% when the timer ends
        # callback(100)
        # time.sleep(2)
        # callback(0)
        #self.callback_reset_status()

        print("\nTimer finished!")  # Optional: Add a message when the timer completes

    def send_time(self):

        return self.remaining_time




