from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        # Distance
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        # Unit dropdown
        self.combo = QComboBox()
        self.combo.addItems(["Metric (km)", "Imperial (miles)"])

        # Time
        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        # Calculate button
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_speed)

        # Output label
        self.result_label = QLabel("Average Speed:")
        grid.addWidget(self.result_label, 3, 0, 1, 3)

        # Layout
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)

        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 1)

        self.setLayout(grid)

    def calculate_speed(self):
        try:
            distance = float(self.distance_line_edit.text())
            time = float(self.time_line_edit.text())

            if time == 0:
                self.result_label.setText("Time cannot be 0")
                return

            speed = distance / time

            if self.combo.currentText() == "Metric (km)":
                speed = round(speed, 2)
                unit = "km/h"
            else:
                speed = round(speed * 0.621371, 2)
                unit = "mph"

            self.result_label.setText(f"Average Speed: {speed} {unit}")

        except ValueError:
            self.result_label.setText("Please enter valid numbers")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
