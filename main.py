from PySide6.QtWidgets import QApplication
from ui.dashboard_window import DashboardWindow  # import the dashboard GUI
import sys

def main():
    app = QApplication(sys.argv)
    
    # Create and show the dashboard window
    dashboard = DashboardWindow()
    dashboard.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
