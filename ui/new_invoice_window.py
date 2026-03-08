# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
#     QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
#     QDateEdit, QGroupBox, QFrame, QScrollArea, QCalendarWidget, QMessageBox
# )
# from PySide6.QtCore import Qt, QDate
# from ui.passenger_window import PassengerWindow
# from ui.flight_window import FlightWindow
# from ui.ticket_window import TicketWindow
# from ui.sections.details_section import DetailsSection
# import sys, os

# class NewInvoiceWindow(QMainWindow):
#     """
#     New Invoice Parent Window
#     - Full screen with gradient background
#     - Header & Footer consistent with dashboard
#     - Sections for Invoice Info, Passengers, Flights, Tickets
#     - Buttons to open child windows for data entry
#     """

#     def __init__(self, invoice_number=None, parent_dashboard=None):
#         super().__init__()
#         self.setWindowTitle("New Invoice")
#         self.showMaximized()
#         self.passenger_data = []  # Will store passenger details from child window
#         self.flight_data = []     # Will store flight details
#         self.ticket_data = []     # Will store ticket details
        
#         self.parent_dashboard = parent_dashboard
#         self.invoice_number.setText(invoice_number)
        
#         self.init_ui()
#         self.load_styles()
#         self.load_agents()

#     # ------------------ UI SETUP ------------------
#     def init_ui(self):
#         """Initialize the UI components and layouts."""
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         main_layout = QVBoxLayout()
#         main_layout.setSpacing(20)
#         main_layout.setContentsMargins(30, 20, 30, 20)
#         main_widget.setLayout(main_layout)

#         # ------------------ HEADER ------------------
#         self.header = QLabel("C WORLD TRAVELS (2012) LTD")
#         self.header.setAlignment(Qt.AlignCenter)
#         self.header.setObjectName("headerLabel")
#         main_layout.addWidget(self.header)

#         # ------------------ SCROLL AREA ------------------
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_content = QWidget()
#         scroll_layout = QVBoxLayout()
#         scroll_layout.setSpacing(30)
#         scroll_content.setLayout(scroll_layout)
#         scroll_area.setWidget(scroll_content)
#         main_layout.addWidget(scroll_area)

#         # ------------------ INVOICE INFO ------------------
#         invoice_group = QGroupBox("Invoice Information")
#         invoice_layout = QHBoxLayout()
#         invoice_group.setLayout(invoice_layout)

#         # Invoice Number (read-only)
#         self.invoice_number = QLabel()
#         self.invoice_number.setAlignment(Qt.AlignCenter)
#         self.invoice_number.setObjectName("invoiceLabel")

#         # PNR Number (editable)
#         self.pnr_input = QLineEdit()
#         self.pnr_input.setObjectName("pnrInput")
#         self.pnr_input.setAlignment(Qt.AlignCenter)
#         self.pnr_input.setFixedWidth(150)

#         # Agent Name dropdown
#         self.agent_combobox = QComboBox()
#         self.agent_combobox.setObjectName("agentCombo")
#         self.agent_combobox.setFixedWidth(200)

#        # Invoice Date
#         self.invoice_date = QDateEdit(QDate.currentDate())
#         self.invoice_date.setCalendarPopup(True)
#         self.invoice_date.setObjectName("dateEdit")
#         self.invoice_date.setFixedWidth(150)

#         # Add widgets to layout with labels
#         invoice_layout.addWidget(QLabel("Invoice Number:"))
#         invoice_layout.addWidget(self.invoice_number)
#         invoice_layout.addSpacing(30)
#         invoice_layout.addWidget(QLabel("PNR Number:"))
#         invoice_layout.addWidget(self.pnr_input)
#         invoice_layout.addSpacing(30)
#         invoice_layout.addWidget(QLabel("Agent Name:"))
#         invoice_layout.addWidget(self.agent_combobox)
#         invoice_layout.addSpacing(30)
#         invoice_layout.addWidget(QLabel("Invoice Date:"))
#         invoice_layout.addWidget(self.invoice_date)
#         invoice_layout.addStretch()

#         # Add to scroll layout
#         scroll_layout.addWidget(invoice_group)

#         # ------------------ PASSENGER SECTION ------------------
#         self.passenger_section = DetailsSection(
#             "Passenger Details",
#             ["Name", "Address", "Contact No"]
#         )
#         self.add_passenger_btn = QPushButton("Add Passenger")
#         self.add_passenger_btn.setObjectName("addPassengerBtn")
        
#         scroll_layout.addWidget(self.passenger_section)
#         self.passenger_section.add_button.clicked.connect(self.add_passenger)

        
#         # # ------------------ PASSENGER SECTION ------------------
#         # passenger_group = QGroupBox("Passenger Details")
#         # passenger_layout = QVBoxLayout()
#         # passenger_group.setLayout(passenger_layout)

#         # self.passenger_table = QTableWidget(0, 3)
#         # self.passenger_table.setHorizontalHeaderLabels(["Name", "Address", "Contact No"])
#         # self.passenger_table.horizontalHeader().setStretchLastSection(True)
#         # self.passenger_table.setEditTriggers(QTableWidget.NoEditTriggers)

#         # passenger_button = QPushButton("Add Passenger")
#         # passenger_button.clicked.connect(self.add_passenger)

#         # passenger_layout.addWidget(self.passenger_table)
#         # passenger_layout.addWidget(passenger_button, alignment=Qt.AlignRight)
#         # scroll_layout.addWidget(passenger_group)

#         # ------------------ FLIGHT SECTION ------------------
#         flight_group = QGroupBox("Flight Details")
#         flight_layout = QVBoxLayout()
#         flight_group.setLayout(flight_layout)

#         self.flight_table = QTableWidget(0, 6)
#         self.flight_table.setHorizontalHeaderLabels(
#             ["Airline", "Flight No", "Departure Date", "Arrival Date", "From", "To"]
#         )
#         self.flight_table.horizontalHeader().setStretchLastSection(True)
#         self.flight_table.setEditTriggers(QTableWidget.NoEditTriggers)

#         self.add_flight_btn = QPushButton("Add Flight")
#         self.add_flight_btn.setObjectName("addFlightBtn")

#         flight_layout.addWidget(self.flight_table)
#         flight_layout.addWidget(self.flight_button, alignment=Qt.AlignRight)
#         scroll_layout.addWidget(flight_group)
        
#         self.flight_button.clicked.connect(self.add_flight)

#         # ------------------ TICKET SECTION ------------------
#         ticket_group = QGroupBox("Ticket Details")
#         ticket_layout = QVBoxLayout()
#         ticket_group.setLayout(ticket_layout)

#         self.ticket_table = QTableWidget(0, 5)
#         self.ticket_table.setHorizontalHeaderLabels(
#             ["Ticket No", "Base Fare", "Other Tax", "GST/HST", "Total"]
#         )
#         self.ticket_table.horizontalHeader().setStretchLastSection(True)
#         self.ticket_table.setEditTriggers(QTableWidget.NoEditTriggers)

#         self.add_ticket_btn = QPushButton("Add Ticket")
#         self.add_ticket_btn.setObjectName("addTicketBtn")

#         ticket_layout.addWidget(self.ticket_table)
#         ticket_layout.addWidget(self.ticket_button, alignment=Qt.AlignRight)
#         scroll_layout.addWidget(ticket_group)
        
#         self.ticket_button.clicked.connect(self.add_ticket)

#         # ------------------ FOOTER BUTTONS ------------------
#         button_layout = QHBoxLayout()
#         button_layout.setSpacing(30)
#         button_layout.addStretch(1)

#         save_final = QPushButton("Save Final Invoice")
#         save_final.clicked.connect(lambda: self.save_invoice(final=True))
#         save_draft = QPushButton("Save Draft")
#         save_draft.clicked.connect(lambda: self.save_invoice(final=False))
#         cancel = QPushButton("Cancel")
#         cancel.clicked.connect(self.close)

#         button_layout.addWidget(save_final)
#         button_layout.addWidget(save_draft)
#         button_layout.addWidget(cancel)
#         scroll_layout.addLayout(button_layout)

#         # ------------------ FOOTER ------------------
#         footer_line = QFrame()
#         footer_line.setFrameShape(QFrame.HLine)
#         footer_line.setObjectName("footerLine")
#         main_layout.addWidget(footer_line)

#         footer_layout = QHBoxLayout()
#         footer_layout.setContentsMargins(30, 0, 30, 10)

#         footer_left = QLabel(
#             "C WORLD TRAVEL (2012) LTD.\n"
#             "Address: 489 Albert St N, Regina, SK, S4R 3C4"
#         )
#         footer_left.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#         footer_left.setObjectName("footerLabel")

#         footer_right = QLabel(
#             "Contact No: +1(306)949-1235\n"
#             "G.S.T: 832336283RP0001"
#         )
#         footer_right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#         footer_right.setObjectName("footerLabel")

#         footer_layout.addWidget(footer_left)
#         footer_layout.addStretch(0)
#         footer_layout.addWidget(footer_right)

#         main_layout.addLayout(footer_layout)

#     # ------------------ LOAD AGENTS FROM FILE ------------------
#     def load_agents(self):
#         """Load agent names from a text file for the dropdown."""
#         agent_file = os.path.join(os.getcwd(), "config", "agents.txt")
#         if os.path.exists(agent_file):
#             with open(agent_file, "r") as f:
#                 agents = [line.strip() for line in f.readlines()]
#             self.agent_combobox.addItems(agents)
#         else:
#             print("agents.txt file not found!")

#     # ------------------ PLACEHOLDER FUNCTIONS FOR CHILD WINDOWS ------------------
#     def add_passenger(self):
#         """Open child window to add passenger (to implement)."""
#         # Placeholder for child window connection
#         self.passenger_window = PassengerWindow(self)
#         self.passenger_window.show()
        
#     def add_flight(self):
#         """Open child window to add flight (to implement)."""
#         self.flight_window = FlightWindow(self)
#         self.flight_window.show()
    
#     def add_ticket(self):
#         """Open child window to add ticket (to implement)."""
#         self.ticket_window = TicketWindow(self)
#         self.ticket_window.show()
    
#     # ------------------ SAVE INVOICE ------------------
#     def save_invoice(self, final=True):
#         """Save invoice data (placeholder)."""
#         QMessageBox.information(
#             self,
#             "Save Invoice",
#             f"{'Final' if final else 'Draft'} invoice saved (functionality to implement)."
#         )

#     # ------------------ LOAD CSS ------------------
#     def load_styles(self):
#         """Load external QSS file for styling."""
#         try:
#             css_path = os.path.join(os.path.dirname(__file__), "../css/invoicedash.qss")
#             with open(css_path, "r") as file:
#                 self.setStyleSheet(file.read())
#         except FileNotFoundError:
#             print("dashboard.qss file not found!")
            
#     # ------------CLOSE EVENT  ------------
#     def closeEvent(self, event):
#         """Restore the dashboard window when closing this window."""
#         if self.parent_dashboard:
#             self.parent_dashboard.show()
#         event.accept()

# # ------------------ MAIN ------------------
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = NewInvoiceWindow()
#     window.show()
#     sys.exit(app.exec())



       # ------------------ PASSENGER SECTION ------------------
        # self.passenger_section = DetailsSection(
        #     "Passenger Details",
        #     ["", "", "Name", "Address", "Contact No"]
        # )
        # self.add_passenger_btn = QPushButton("Add Passenger")
        # self.add_passenger_btn.setObjectName("addPassengerBtn")  # ✅ matches QSS

        # passenger_button_layout = QHBoxLayout()
        # passenger_button_layout.addStretch()
        # passenger_button_layout.addWidget(self.add_passenger_btn)

        # scroll_layout.addWidget(self.passenger_section)
        # scroll_layout.addLayout(passenger_button_layout)
        # self.add_passenger_btn.clicked.connect(self.add_passenger)
        
        # --- PASSENGER SECTION ---
        # self.passenger_section = DetailsSection(
        #     "Passenger Details",
        #     ["", "", "Name", "Address", "Contact No"],
        #     parent=self
        # )
        
        # self.add_passenger_btn = QPushButton("Add Passenger")
        # self.add_passenger_btn.setObjectName("addPassengerBtn")  # ✅ matches QSS

        # passenger_button_layout = QHBoxLayout()
        # passenger_button_layout.addStretch()
        # passenger_button_layout.addWidget(self.add_passenger_btn)

        # # Add the section directly to layout (no extra Add button needed)
        # scroll_layout.addWidget(self.passenger_section)

        # # Connect the built-in 'Add' button from DetailsSection
        # self.add_passenger_btn.clicked.connect(self.add_passenger)
        

        # # ------------------ FLIGHT SECTION ------------------
        # flight_group = QGroupBox("Flight Details")
        # flight_layout = QVBoxLayout()
        # flight_group.setLayout(flight_layout)

        # self.flight_table = QTableWidget(0, 6)
        # self.flight_table.setHorizontalHeaderLabels(
        #     ["Airline", "Flight No", "Departure Date", "Arrival Date", "From", "To"]
        # )
        # self.flight_table.horizontalHeader().setStretchLastSection(True)
        # self.flight_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # self.add_flight_btn = QPushButton("Add Flight")
        # self.add_flight_btn.setObjectName("addFlightBtn")  # ✅ matches QSS

        # flight_button_layout = QHBoxLayout()
        # flight_button_layout.addStretch()
        # flight_button_layout.addWidget(self.add_flight_btn)

        # flight_layout.addWidget(self.flight_table)
        # flight_layout.addLayout(flight_button_layout)
        # scroll_layout.addWidget(flight_group)

        # self.add_flight_btn.clicked.connect(self.add_flight)

        # # ------------------ TICKET SECTION ------------------
        # ticket_group = QGroupBox("Ticket Details")
        # ticket_layout = QVBoxLayout()
        # ticket_group.setLayout(ticket_layout)

        # self.ticket_table = QTableWidget(0, 5)
        # self.ticket_table.setHorizontalHeaderLabels(
        #     ["Ticket No", "Base Fare", "Other Tax", "GST/HST", "Total"]
        # )
        # self.ticket_table.horizontalHeader().setStretchLastSection(True)
        # self.ticket_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # self.add_ticket_btn = QPushButton("Add Ticket")
        # self.add_ticket_btn.setObjectName("addTicketBtn")  # ✅ matches QSS

        # ticket_button_layout = QHBoxLayout()
        # ticket_button_layout.addStretch()
        # ticket_button_layout.addWidget(self.add_ticket_btn)

        # ticket_layout.addWidget(self.ticket_table)
        # ticket_layout.addLayout(ticket_button_layout)
        # scroll_layout.addWidget(ticket_group)

        # self.add_ticket_btn.clicked.connect(self.add_ticket)


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
    QDateEdit, QGroupBox, QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from ui.passenger_window import PassengerWindow
from ui.flight_window import FlightWindow
from ui.ticket_window import TicketWindow
from ui.sections.passenger_section import PassengerSection
from ui.sections.flight_section import FlightSection
from ui.sections.ticket_section import TicketSection
import sys, os


class NewInvoiceWindow(QMainWindow):
    """Invoice window with sections for passengers, flights, and tickets."""

    def __init__(self, invoice_number=None, parent_dashboard=None):
        super().__init__()
        self.setWindowTitle("New Invoice")
        self.showMaximized()

        # Initialize data containers
        self.passenger_data = []
        self.flight_data = []
        self.ticket_data = []

        self.parent_dashboard = parent_dashboard
        self.invoice_number_value = invoice_number or "INV-0001"

        self.init_ui()
        self.load_styles()
        self.load_agents()

    # ------------------ UI SETUP ------------------
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_widget.setLayout(main_layout)

        # ------------------ HEADER ------------------
        header = QLabel("C WORLD TRAVELS (2012) LTD")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("headerLabel")
        main_layout.addWidget(header)

        # ------------------ SCROLL AREA ------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(30)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # ------------------ INVOICE INFO ------------------
        invoice_group = QGroupBox("Invoice Information")
        invoice_layout = QHBoxLayout()
        invoice_group.setLayout(invoice_layout)

        self.invoice_number = QLabel(self.invoice_number_value)
        self.invoice_number.setAlignment(Qt.AlignCenter)
        self.invoice_number.setObjectName("invoiceLabel")

        self.pnr_input = QLineEdit()
        self.pnr_input.setAlignment(Qt.AlignCenter)
        self.pnr_input.setFixedWidth(150)

        self.agent_combobox = QComboBox()
        self.agent_combobox.setFixedWidth(200)

        self.invoice_date = QDateEdit(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setFixedWidth(150)

        invoice_layout.addWidget(QLabel("Invoice Number:"))
        invoice_layout.addWidget(self.invoice_number)
        invoice_layout.addSpacing(30)
        invoice_layout.addWidget(QLabel("PNR Number:"))
        invoice_layout.addWidget(self.pnr_input)
        invoice_layout.addSpacing(30)
        invoice_layout.addWidget(QLabel("Agent Name:"))
        invoice_layout.addWidget(self.agent_combobox)
        invoice_layout.addSpacing(30)
        invoice_layout.addWidget(QLabel("Invoice Date:"))
        invoice_layout.addWidget(self.invoice_date)
        invoice_layout.addStretch()

        scroll_layout.addWidget(invoice_group)

 
        # ------------------ PASSENGER SECTION ------------------
        self.passenger_section = PassengerSection(self)
        scroll_layout.addWidget(self.passenger_section)
        self.passenger_section.add_btn.clicked.connect(self.add_passenger)
        
        # ------------------ FLIGHT SECTION ------------------
        self.flight_section = FlightSection(self)
        scroll_layout.addWidget(self.flight_section)
        self.flight_section.add_btn.clicked.connect(self.add_flight)

        # ------------------ TICKET SECTION ------------------
        self.ticket_section = TicketSection(self)
        scroll_layout.addWidget(self.ticket_section)
        self.ticket_section.add_btn.clicked.connect(self.add_ticket)

        # ------------------ FOOTER BUTTONS ------------------
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        button_layout.addStretch(1)

        save_final = QPushButton("Save Final Invoice")
        save_draft = QPushButton("Save Draft")
        cancel = QPushButton("Cancel")

        save_final.clicked.connect(lambda: self.save_invoice(final=True))
        save_draft.clicked.connect(lambda: self.save_invoice(final=False))
        cancel.clicked.connect(self.close)

        button_layout.addWidget(save_final)
        button_layout.addWidget(save_draft)
        button_layout.addWidget(cancel)
        scroll_layout.addLayout(button_layout)

        # ------------------ FOOTER ------------------
        footer_line = QFrame()
        footer_line.setFrameShape(QFrame.HLine)
        main_layout.addWidget(footer_line)

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(30, 0, 30, 10)

        footer_left = QLabel(
            "C WORLD TRAVEL (2012) LTD.\n"
            "Address: 489 Albert St N, Regina, SK, S4R 3C4"
        )
        footer_right = QLabel(
            "Contact No: +1(306)949-1235\nG.S.T: 832336283RP0001"
        )
        footer_left.setAlignment(Qt.AlignLeft)
        footer_right.setAlignment(Qt.AlignRight)

        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)

        main_layout.addLayout(footer_layout)

    # ------------------ LOAD AGENTS ------------------
    def load_agents(self):
        path = os.path.join(os.getcwd(), "config", "agents.txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                self.agent_combobox.addItems([line.strip() for line in f.readlines()])
        else:
            print("agents.txt not found")

    # ------------------ CHILD WINDOWS ------------------
    def add_passenger(self):
        self.passenger_window = PassengerWindow(self)
        self.passenger_window.show()

    def add_flight(self):
        self.flight_window = FlightWindow(self)
        self.flight_window.show()

    def add_ticket(self):
        self.ticket_window = TicketWindow(self)
        self.ticket_window.show()

    # ------------------ SAVE ------------------
    def save_invoice(self, final=True):
        QMessageBox.information(self, "Save Invoice", f"{'Final' if final else 'Draft'} invoice saved.")

    # ------------------ STYLE ------------------
    def load_styles(self):
        """Load external QSS file for styling."""
        try:
            css_path = os.path.join(os.path.dirname(__file__), "../css/invoicedash.qss")
            with open(css_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("dashboard.qss file not found!")

    # ------------------ CLOSE EVENT ------------------
    def closeEvent(self, event):
        if self.parent_dashboard:
            self.parent_dashboard.show()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewInvoiceWindow()
    window.show()
    sys.exit(app.exec())



