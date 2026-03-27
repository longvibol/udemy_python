from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys

from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        distance_label = QLabel("Distance:")
        distance_line_edit = QLineEdit()

        combo = QComboBox()
        combo.addItems(['Metric(km)', 'Inch'])

        if combo.currentText() == 'Metric(km)':
            "do something"
        if combo.currentText() == 'Inch':
            "do something else"

        Time_label = QLabel("Time(hours):")
        Time_label_line_edit = QLineEdit()

        self.date_birth_line_edit = QLineEdit()

        # Button Calculate
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.metric_cal)
        self.Metric_output_label = QLabel("")

        # Add widget to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(distance_line_edit, 0, 1)

        # Drop box
        grid.addWidget(combo, 0, 2)
        grid.addWidget(self.date_birth_line_edit, 1, 1)

        # Time Display
        grid.addWidget(Time_label, 1, 0)
        grid.addWidget(Time_label_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1, 1, 1)
        grid.addWidget(self.Metric_output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def metric_cal(self):

       self.Metric_output_label.setText(f"Average Speed: ")

app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())

