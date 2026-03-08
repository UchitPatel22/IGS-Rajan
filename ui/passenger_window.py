# # ui/passenger_window.py
# from PySide6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
#     QTableWidget, QTableWidgetItem, QScrollArea, QMessageBox
# )
# from PySide6.QtCore import Qt

# class PassengerWindow(QWidget):
#     def __init__(self, parent_invoice=None):
#         super().__init__()
#         self.setWindowTitle("Add Passenger")
#         self.resize(700, 500)
#         self.parent_invoice = parent_invoice
#         self.passenger_data = []  # store unsaved passenger rows

#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout(self)

#         # ---------------- INPUT FIELDS ----------------
#         form_layout = QHBoxLayout()

#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Name")
#         form_layout.addWidget(QLabel("Name:"))
#         form_layout.addWidget(self.name_input)

#         self.address_input = QLineEdit()
#         self.address_input.setPlaceholderText("Address")
#         form_layout.addWidget(QLabel("Address:"))
#         form_layout.addWidget(self.address_input)

#         self.contact_input = QLineEdit()
#         self.contact_input.setPlaceholderText("Contact No")
#         form_layout.addWidget(QLabel("Contact No:"))
#         form_layout.addWidget(self.contact_input)

#         layout.addLayout(form_layout)

#         # ---------------- TABLE DISPLAY ----------------
#         self.table = QTableWidget(0, 3)
#         self.table.setHorizontalHeaderLabels(["Name", "Address", "Contact No"])
#         self.table.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.table.setAlternatingRowColors(True)
#         self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         layout.addWidget(self.table)

#         # ---------------- BUTTONS ----------------
#         btn_layout = QHBoxLayout()
#         add_btn = QPushButton("Add")
#         add_btn.clicked.connect(self.add_passenger)
#         save_btn = QPushButton("Save")
#         save_btn.clicked.connect(self.save_passengers)
#         btn_layout.addWidget(add_btn)
#         btn_layout.addWidget(save_btn)
#         layout.addLayout(btn_layout)

#     def add_passenger(self):
#         """Add passenger to local table (not yet DB)."""
#         name = self.name_input.text().strip()
#         address = self.address_input.text().strip()
#         contact = self.contact_input.text().strip()

#         if not name:
#             QMessageBox.warning(self, "Input Error", "Name is required")
#             return

#         row = [name, address, contact]
#         self.passenger_data.append(row)

#         # Add to display table
#         row_pos = self.table.rowCount()
#         self.table.insertRow(row_pos)
#         for col, value in enumerate(row):
#             self.table.setItem(row_pos, col, QTableWidgetItem(value))

#         # Clear inputs
#         self.name_input.clear()
#         self.address_input.clear()
#         self.contact_input.clear()

#     def save_passengers(self):
#         """Save to parent window table (later add DB insert here)."""
#         if self.parent_invoice:
#             for row in self.passenger_data:
#                 # Add row using the generic DetailsSection helper
#                 self.parent_invoice.passenger_section.add_row(row)

#             # Also sync parent list
#             self.parent_invoice.passenger_data.extend(self.passenger_data)

#         QMessageBox.information(self, "Success", "Passengers saved successfully.")
#         self.close()



from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
import sys, os


class PassengerWindow(QWidget):
    def __init__(self, parent_invoice=None):
        super().__init__()
        self.setWindowTitle("Add Passenger")
        self.resize(1300, 550)
        self.parent_invoice = parent_invoice
        self.passenger_data = []  # store unsaved passenger rows

        # self.init_ui()
        # self.load_styles()
        
         # ✅ Wrap everything inside a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        self.init_ui(main_layout)

        # Outer layout to hold scroll area
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll)

        self.load_styles()

    def init_ui(self, layout):
        layout = QVBoxLayout(self)

        # ---------------- INPUT FIELDS ----------------
        form_layout = QHBoxLayout()

        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)

        # Contact No
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact No")
        form_layout.addWidget(QLabel("Contact No:"))
        form_layout.addWidget(self.contact_input)

        # Email (optional)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (optional)")
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)

        # Address (moved to end and wider)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Full Address")
        form_layout.addWidget(QLabel("Address:"))
        form_layout.addWidget(self.address_input, stretch=2)

        layout.addLayout(form_layout)

        # ---------------- TABLE DISPLAY ----------------
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Contact No", "Email", "Address"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # Scrollbars always visible
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.table.setWordWrap(False)

        # Make Address column stretch to fill window
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 150)  # Name
        header.resizeSection(1, 120)  # Contact
        header.resizeSection(2, 180)  # Email

        layout.addWidget(self.table)

        # ---------------- BUTTONS ----------------
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_passenger)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_passengers)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def add_passenger(self):
        """Add passenger to local table (not yet DB)."""
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Name is required")
            return

        row = [name, contact, email, address]
        self.passenger_data.append(row)

        # Add to display table
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        for col, value in enumerate(row):
            self.table.setItem(row_pos, col, QTableWidgetItem(value))

        # Clear inputs after adding
        self.name_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    def save_passengers(self):
        """Save to parent window table (later add DB insert here)."""
        if self.parent_invoice:
            for row in self.passenger_data:
                # Add row using the generic DetailsSection helper
                self.parent_invoice.passenger_section.add_row(row)

            # Also sync parent list
            self.parent_invoice.passenger_data.extend(self.passenger_data)

        QMessageBox.information(self, "Success", "Passengers saved successfully.")
        self.close()

    # ------------------ LOAD CSS ------------------
    def load_styles(self):
        """Load external QSS file for styling."""
        try:
            css_path = os.path.join(os.path.dirname(__file__), "../css/passanger.qss")
            with open(css_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("dashboard.qss file not found!")


