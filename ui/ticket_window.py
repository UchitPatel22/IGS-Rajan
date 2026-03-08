# ui/ticket_window.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout

class TicketWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Ticket")
        self.setMinimumSize(400, 300)

        # Form Layout
        form_layout = QFormLayout()

        self.ticket_number_input = QLineEdit()
        self.passenger_name_input = QLineEdit()
        self.flight_number_input = QLineEdit()
        self.price_input = QLineEdit()

        form_layout.addRow("Ticket Number:", self.ticket_number_input)
        form_layout.addRow("Passenger Name:", self.passenger_name_input)
        form_layout.addRow("Flight Number:", self.flight_number_input)
        form_layout.addRow("Price:", self.price_input)

        # Save button
        self.save_btn = QPushButton("Save")

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

