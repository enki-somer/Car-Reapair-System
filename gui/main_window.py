from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from .workers_ui import WorkerManagementUI
from .attendance_ui import AttendanceUI
from .sales_ui import SalesUI
from .inventory_ui import InventoryUI
from .reporting_ui import ReportingUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("نظام إدارة الورشة")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#logoutBtn {
                background-color: #e74c3c;
                margin: 10px;
                min-width: 120px;
            }
            QPushButton#logoutBtn:hover {
                background-color: #c0392b;
            }
            QPushButton#reportsBtn {
                background-color: #9b59b6;
            }
            QPushButton#reportsBtn:hover {
                background-color: #8e44ad;
            }
        """)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Logout button at the top
        top_layout = QHBoxLayout()
        self.logout_btn = QPushButton("تسجيل الخروج", self)
        self.logout_btn.setObjectName("logoutBtn")
        self.logout_btn.setIcon(QIcon("icons/logout.png"))
        self.logout_btn.setIconSize(QSize(20, 20))
        self.logout_btn.clicked.connect(self.logout)
        top_layout.addWidget(self.logout_btn)
        top_layout.addStretch()  # Push logout button to the right
        main_layout.addLayout(top_layout)

        # Navigation buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(20)

        # Add navigation buttons
        self.inventory_button = QPushButton("إدارة المخزون", self)
        self.inventory_button.setIcon(QIcon("icons/inventory.png"))
        self.inventory_button.setIconSize(QSize(24, 24))
        self.inventory_button.clicked.connect(self.open_inventory_management)

        self.sales_button = QPushButton("إدارة المبيعات", self)
        self.sales_button.setIcon(QIcon("icons/sales.png"))
        self.sales_button.setIconSize(QSize(24, 24))
        self.sales_button.clicked.connect(self.open_sales_management)

        self.reports_button = QPushButton("التقارير", self)
        self.reports_button.setObjectName("reportsBtn")
        self.reports_button.setIcon(QIcon("icons/reports.png"))
        self.reports_button.setIconSize(QSize(24, 24))
        self.reports_button.clicked.connect(self.open_reports)

        self.worker_management_button = QPushButton("إدارة الموظفين", self)
        self.worker_management_button.setIcon(QIcon("icons/workers.png"))
        self.worker_management_button.setIconSize(QSize(24, 24))
        self.worker_management_button.clicked.connect(self.open_worker_management)
        
        self.attendance_button = QPushButton("إدارة الحضور", self)
        self.attendance_button.setIcon(QIcon("icons/attendance.png"))
        self.attendance_button.setIconSize(QSize(24, 24))
        self.attendance_button.clicked.connect(self.open_attendance_management)

        buttons_layout.addStretch()  # Space at top
        buttons_layout.addWidget(self.inventory_button)
        buttons_layout.addWidget(self.sales_button)
        buttons_layout.addWidget(self.reports_button)  # Add reports button
        buttons_layout.addWidget(self.worker_management_button)
        buttons_layout.addWidget(self.attendance_button)
        buttons_layout.addStretch()  # Space at bottom

        main_layout.addLayout(buttons_layout)

        # Store window references
        self.inventory_window = None
        self.sales_window = None
        self.reports_window = None
        self.worker_management_ui = None
        self.attendance_ui = None

    def open_inventory_management(self):
        """فتح نافذة إدارة المخزون"""
        if not self.inventory_window:
            self.inventory_window = InventoryUI()
        self.inventory_window.show()

    def open_sales_management(self):
        """فتح نافذة إدارة المبيعات"""
        if not self.sales_window:
            self.sales_window = SalesUI()
            # Connect to reports window if it exists
            if self.reports_window:
                self.sales_window.sale_completed.connect(self.reports_window.refresh_report)
        self.sales_window.show()

    def open_reports(self):
        """فتح نافذة التقارير"""
        if not self.reports_window:
            self.reports_window = ReportingUI()
            # Connect to sales window if it exists
            if self.sales_window:
                self.sales_window.sale_completed.connect(self.reports_window.refresh_report)
        self.reports_window.show()

    def open_worker_management(self):
        self.worker_management_ui = WorkerManagementUI()
        self.worker_management_ui.exec_()

    def open_attendance_management(self):
        self.attendance_ui = AttendanceUI()
        self.attendance_ui.exec_()

    def logout(self):
        reply = QMessageBox.question(
            self, 
            "تأكيد تسجيل الخروج",
            "هل أنت متأكد من تسجيل الخروج؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Close all windows
            if self.inventory_window:
                self.inventory_window.close()
            if self.sales_window:
                self.sales_window.close()
            if self.reports_window:
                self.reports_window.close()
            # Close the main window and show login window
            from .login_ui import LoginUI
            self.close()
            login = LoginUI()
            if login.exec_() == LoginUI.Accepted:
                self.show()
            else:
                import sys
                sys.exit()
