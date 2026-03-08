from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QGroupBox, QTableWidgetItem
from PySide6.QtCore import Qt

class PassengerSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.group = QGroupBox("Passenger Details")
        group_layout = QVBoxLayout()
        self.group.setLayout(group_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["", "", "Name", "Address", "Contact No"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # ✅ Scroll setup
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setWordWrap(False)
        
        group_layout.addWidget(self.table)

        self.add_btn = QPushButton("Add Passenger")
        self.add_btn.setObjectName("addPassengerBtn")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_btn)
        group_layout.addLayout(btn_layout)

        layout.addWidget(self.group)

    def add_row(self, data):
        """Adds ticket data row."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, value in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(value))
