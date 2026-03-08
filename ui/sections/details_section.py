# # ui/sections/details_section.py
# from PySide6.QtWidgets import (
#     QGroupBox, QVBoxLayout, QTableWidget, QPushButton,
#     QHBoxLayout, QWidget, QTableWidgetItem
# )
# from PySide6.QtCore import Qt
# from ui.passenger_window import PassengerWindow


# class DetailsSection(QGroupBox):
#     def __init__(self, title, headers, parent=None):
#         """
#         Generic Section Widget
#         :param title: Section Title (str)
#         :param headers: List of column headers (without Actions column)
#         """
#         super().__init__(title, parent)
#         self.headers = headers

#         layout = QVBoxLayout(self)

#         # Table with +1 column for Actions
#         self.table = QTableWidget(0, len(headers) + 1)
#         self.table.setHorizontalHeaderLabels(headers + ["Actions"])
#         self.table.horizontalHeader().setStretchLastSection(True)
#         self.table.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.table.setMinimumHeight(180)  # show ~5 rows
#         layout.addWidget(self.table)

#         # # Add Button
#         # self.add_button = QPushButton(f"Add {title.split()[0]}")
#         # layout.addWidget(self.add_button, alignment=Qt.AlignRight)

#     # --- Add row ---
#     def add_row(self, row_data):
#         """
#         Add new row.
#         :param row_data: list of values matching headers
#         """
#         if len(row_data) != len(self.headers):
#             raise ValueError("Row data must match number of headers")

#         row = self.table.rowCount()
#         self.table.insertRow(row)

#         # Fill data
#         for col, value in enumerate(row_data):
#             self.table.setItem(row, col, QTableWidgetItem(str(value)))

#         # Add action buttons
#         self._add_action_buttons(row)

#     def _add_action_buttons(self, row):
#         action_layout = QHBoxLayout()
#         edit_btn = QPushButton("✏️")
#         delete_btn = QPushButton("🗑️")
#         edit_btn.setFixedSize(30, 25)
#         delete_btn.setFixedSize(30, 25)

#         edit_btn.clicked.connect(lambda _, r=row: self.edit_row(r))
#         delete_btn.clicked.connect(lambda _, r=row: self.delete_row(r))

#         action_widget = QWidget()
#         action_layout.addWidget(edit_btn)
#         action_layout.addWidget(delete_btn)
#         action_layout.setContentsMargins(0, 0, 0, 0)
#         action_layout.setAlignment(Qt.AlignCenter)
#         action_widget.setLayout(action_layout)

#         self.table.setCellWidget(row, len(self.headers), action_widget)

#     # --- Edit row (stub, can be overridden) ---
#     def edit_row(self, row):
#         data = [self.table.item(row, col).text() for col in range(len(self.headers))]
#         # Open child window and pass `data` and `row` index
#         self.edit_window = PassengerWindow(self.parent, data, row)
#         self.edit_window.show()

#     # --- Delete row ---
#     def delete_row(self, row):
#         self.table.removeRow(row)

#     # --- Get all rows ---
#     def get_all_rows(self):
#         all_data = []
#         for row in range(self.table.rowCount()):
#             row_data = [
#                 self.table.item(row, col).text() if self.table.item(row, col) else ""
#                 for col in range(len(self.headers))
#             ]
#             all_data.append(row_data)
#         return all_data
