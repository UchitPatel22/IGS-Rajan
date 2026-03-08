# ui/flight_window.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout

class FlightWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Flight")
        self.setMinimumSize(400, 300)

        # Form Layout
        form_layout = QFormLayout()

        self.flight_number_input = QLineEdit()
        self.airline_input = QLineEdit()
        self.origin_input = QLineEdit()
        self.destination_input = QLineEdit()

        form_layout.addRow("Flight Number:", self.flight_number_input)
        form_layout.addRow("Airline:", self.airline_input)
        form_layout.addRow("Origin:", self.origin_input)
        form_layout.addRow("Destination:", self.destination_input)

        # Save button
        self.save_btn = QPushButton("Save")

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

