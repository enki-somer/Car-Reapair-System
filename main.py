import sys
from PyQt5.QtWidgets import QApplication
from gui.login_ui import LoginUI
from gui.main_window import MainWindow
from database.db_setup import init_db

def main():
    # Initialize database and create all tables
    init_db()
    
    app = QApplication(sys.argv)
    
    # Show login dialog
    login = LoginUI()
    if login.exec_() == LoginUI.Accepted:
        # If login successful, show main window
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()