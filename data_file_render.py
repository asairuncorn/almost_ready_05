import csv
import json

class DataLogger:
    def __init__(self, file_name, file_type='csv'):
        """
        Initialize the DataLogger class.

        Args:
            file_name (str): The name of the file where data will be logged.
            file_type (str): The type of file ('csv' or 'json'). Default is 'csv'.
        """
        self.file_name = file_name
        self.file_type = file_type
        self.data = []  # To store rows of data

        # Ensure the file starts fresh if it already exists
        if self.file_type == 'csv':
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([])  # Write an empty header initially
        elif self.file_type == 'json':
            with open(self.file_name, 'w') as file:
                json.dump([], file)

    def log_data(self, **kwargs):
        """
        Log data using named variables (key-value pairs).

        Args:
            **kwargs: Arbitrary keyword arguments representing data fields.
        """
        self.data.append(kwargs)
        self._write_to_file(kwargs)

    def _write_to_file(self, row):
        """
        Write a single row of data to the file.

        Args:
            row (dict): The data row to write.
        """
        if self.file_type == 'csv':
            self._write_csv(row)
        elif self.file_type == 'json':
            self._write_json()

    def _write_csv(self, row):
        """
        Write a row to a CSV file.

        Args:
            row (dict): The data row to write.
        """
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=row.keys())
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(row)

    def _write_json(self):
        """
        Write the entire data to a JSON file.
        """
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)

    def display_data(self):
        """Display all logged data."""
        for row in self.data:
            print(row)


# # Example Usage
# if __name__ == "__main__":
#     logger = DataLogger('data_log.csv', file_type='csv')  # Initialize for CSV file
#
#     # Log some data
#     logger.log_data(sensor1=0.485, sensor2=0.605, status="Running", timestamp="2024-11-19T15:34:00")
#     logger.log_data(sensor1=0.533, sensor2=0.533, status="Idle", timestamp="2024-11-19T15:35:00")
#
#     # Display logged data
#     logger.display_data()
#
#     # Create another logger for JSON
#     json_logger = DataLogger('data_log.json', file_type='json')
#     json_logger.log_data(sensor1=0.485, sensor2=0.605, status="Running", timestamp="2024-11-19T15:34:00")
#     json_logger.log_data(sensor1=0.533, sensor2=0.533, status="Idle", timestamp="2024-11-19T15:35:00")
#     json_logger.display_data()
