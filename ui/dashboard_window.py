# ui/dashboard_window.py
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
import sys
import os
from core.db_manager import DatabaseManager
# from ui.new_invoice_window import NewInvoiceWindow

class DashboardWindow(QMainWindow):
    """
    Professional Invoice Management Dashboard
    - Full-screen layout
    - Gradient background
    - Header, footer, invoice input label fully blend with background
    - Action buttons: New, Edit, View, Deleted
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Management Dashboard")
        self.showMaximized()  # Full-screen
        self.init_ui()
        self.load_styles()
        self.show_next_invoice_number()

    # -------------------------
    # UI SETUP
    # -------------------------
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(50)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_widget.setLayout(main_layout)

        # Header
        self.header = QLabel("C WORLD TRAVELS (2012) LTD")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setObjectName("headerLabel")
        main_layout.addWidget(self.header)

        # Invoice Number Input
        invoice_layout = QVBoxLayout()
        invoice_layout.setAlignment(Qt.AlignCenter)

        self.invoice_label = QLabel("Enter Invoice Number (required for Edit, View, Deleted):")
        self.invoice_label.setAlignment(Qt.AlignCenter)
        self.invoice_label.setStyleSheet("font-size: 16px;")
        self.invoice_label.setObjectName("invoiceLabel")

        self.invoice_input = QLineEdit()
        self.invoice_input.setObjectName("invoiceInput")
        self.invoice_input.setAlignment(Qt.AlignCenter)

        invoice_layout.addWidget(self.invoice_label)
        invoice_layout.addWidget(self.invoice_input)
        main_layout.addLayout(invoice_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        button_layout.setAlignment(Qt.AlignCenter)

        self.new_btn = QPushButton("New")
        self.new_btn.setObjectName("newBtn")
        self.new_btn.clicked.connect(lambda: self.proceed_clicked("New"))

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("editBtn")
        self.edit_btn.clicked.connect(lambda: self.proceed_clicked("Edit"))

        self.view_btn = QPushButton("View")
        self.view_btn.setObjectName("viewBtn")
        self.view_btn.clicked.connect(lambda: self.proceed_clicked("View"))

        self.deleted_btn = QPushButton("Deleted")
        self.deleted_btn.setObjectName("deletedBtn")
        self.deleted_btn.clicked.connect(lambda: self.proceed_clicked("Deleted"))

        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.view_btn)
        button_layout.addWidget(self.deleted_btn)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        # Footer
        footer_line = QFrame()
        footer_line.setFrameShape(QFrame.HLine)
        footer_line.setObjectName("footerLine")
        main_layout.addWidget(footer_line)

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(50, 0, 50, 10)

        footer_left = QLabel(
            "C WORLD TRAVEL (2012) LTD.\n"
            "Address: 489 Albert St N, Regina, SK, S4R 3C4"
        )
        footer_left.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        footer_left.setObjectName("footerLabel")

        footer_right = QLabel(
            "Contact No: +1(306)949-1235\n"
            "G.S.T: 832336283RP0001"
        )
        footer_right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        footer_right.setObjectName("footerLabel")

        footer_layout.addWidget(footer_left)
        footer_layout.addStretch(0)
        footer_layout.addWidget(footer_right)

        main_layout.addLayout(footer_layout)

    # -------------------------
    # BUTTON LOGIC
    # -------------------------
    
    def proceed_clicked(self, action: str):
        """
        Handles button clicks.
        Invoice number is required for all actions except 'New'.
        """
        invoice_number = self.invoice_input.text().strip()

        if action != "New" and not invoice_number:
            QMessageBox.warning(
                self,
                "Input Required",
                f"Please enter an invoice number for {action}."
            )
            return

        # if action == "New":
        #     # Hide dashboard
        #     # Open New Invoice Window
        #     self.new_invoice_window = NewInvoiceWindow(invoice_number)
        #     self.new_invoice_window.show()
        #     self.hide()
        #     return
        
        if action == "New":
            
            # Open New Invoice Window and hide dashboard
            from ui.new_invoice_window import NewInvoiceWindow

            self.new_invoice_window = NewInvoiceWindow(
                invoice_number=invoice_number, 
                parent_dashboard=self
            )
            self.new_invoice_window.show()
            self.hide()
            return

        # For Edit/View/Deleted just show info for now
        QMessageBox.information(
            self,
            "Next Step",
            f"Selected Action: {action}\nInvoice Number: {invoice_number}"
        )

    # -------------------------
    # LOAD CSS
    # -------------------------
    def load_styles(self):
        """Load external CSS styles for dashboard."""
        try:
            css_path = os.path.join(os.path.dirname(__file__), "../css/dashboard1.qss")
            with open(css_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("dashboard.qss file not found! Make sure CSS file exists.")

    # -------------------------
    # AUTO-GENERATE NEXT INVOICE NUMBER
    # -------------------------
    def show_next_invoice_number(self):
        """
        Fetches the last invoice number from the DB and auto-generates the next one.
        - Uses config/invoice_format.txt if no invoice exists.
        - Example: Last = CWT0005 → Next = CWT0006
        """
        db = DatabaseManager("final")
        last_invoice = db.get_last_invoice_number()

        # Path to user config file
        config_path = os.path.join(os.getcwd(), "config", "invoice_format.txt")

        if last_invoice:
            # Split letters and number
            prefix = ''.join(filter(str.isalpha, last_invoice))
            number = ''.join(filter(str.isdigit, last_invoice))
            next_number = int(number) + 1 if number else 1
            new_invoice = f"{prefix}{next_number:04d}"
        else:
            # Read starting invoice number from file
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    start_invoice = f.read().strip()
                if start_invoice:
                    new_invoice = start_invoice
                else:
                    new_invoice = "CWT0001"
            else:
                new_invoice = "CWT0001"

        self.invoice_input.setText(new_invoice)





