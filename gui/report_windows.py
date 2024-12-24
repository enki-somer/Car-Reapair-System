from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QDateEdit, QMessageBox, QHeaderView,
    QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
from app.reports import AttendanceReports
import calendar
from datetime import datetime

class DailyReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_table_behavior()
        self.reports = AttendanceReports()

    def init_ui(self):
        self.setWindowTitle("التقرير اليومي")
        self.setGeometry(200, 200, 1000, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QGroupBox {
                border: 2px solid #dcdde1;
                border-radius: 8px;
                margin-top: 1em;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTableWidget {
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e8e8e8;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e8e8e8;
                border-right: 1px solid #e8e8e8;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #dcdde1;
                border-right: 1px solid #dcdde1;
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
            }
            QTableWidget::item:hover {
                background-color: #f0f6fc;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f9fa;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #95a5a6;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QDateEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                min-width: 120px;
            }
        """)

        layout = QVBoxLayout(self)

        # Back to Home button
        back_layout = QHBoxLayout()
        self.back_btn = QPushButton("العودة للرئيسية")
        self.back_btn.setIcon(QIcon("icons/home.png"))
        self.back_btn.setIconSize(QSize(24, 24))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
                text-align: center;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        self.back_btn.setToolTip("العودة للرئيسية")
        self.back_btn.clicked.connect(self.go_back_home)
        back_layout.addWidget(self.back_btn)
        back_layout.addStretch()
        layout.insertLayout(0, back_layout)

        # Title
        title = QLabel("التقرير اليومي للحضور")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        # Controls
        controls_layout = QHBoxLayout()
        
        date_label = QLabel("اختر التاريخ:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        
        self.generate_btn = QPushButton("عرض التقرير")
        self.generate_btn.setIcon(QIcon("icons/report.png"))
        self.generate_btn.clicked.connect(self.generate_report)
        
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self.date_edit)
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)

        # Report Table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([
            "اسم الموظف", "رقم الهاتف", "وقت الحضور", "وقت الانصراف", "الحالة"
        ])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.setAlternatingRowColors(True)
        layout.addWidget(self.report_table)

        # Print Button
        button_layout = QHBoxLayout()
        self.print_btn = QPushButton("طباعة التقرير")
        self.print_btn.setIcon(QIcon("icons/print.png"))
        self.print_btn.clicked.connect(self.print_report)
        button_layout.addStretch()
        button_layout.addWidget(self.print_btn)
        layout.addLayout(button_layout)

    def setup_table_behavior(self):
        """Setup enhanced table behavior"""
        # Make the entire row selectable
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        # Allow only one row to be selected at a time
        self.report_table.setSelectionMode(QTableWidget.SingleSelection)
        # Set row height
        self.report_table.verticalHeader().setDefaultSectionSize(50)
        # Hide vertical header (row numbers)
        self.report_table.verticalHeader().setVisible(False)
        # Make the table more responsive
        self.report_table.setMouseTracking(True)
        # Set text alignment for all columns
        self.report_table.setLayoutDirection(Qt.RightToLeft)
        # Set alternating row colors
        self.report_table.setAlternatingRowColors(True)

    def generate_report(self):
        date = self.date_edit.date().toPyDate()
        report_data = self.reports.generate_daily_report(date)
        
        if report_data:
            self.report_table.setRowCount(0)
            for row_num, row in enumerate(report_data):
                self.report_table.insertRow(row_num)
                
                # Create items with proper values (removed daily salary)
                values = [
                    row['name'],
                    row['phone'],
                    str(row['time_in'] or ''),
                    str(row['time_out'] or ''),
                    row['status']
                ]
                
                # Set items in table with center alignment
                for col, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.report_table.setItem(row_num, col, item)

    def print_report(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "تنبيه", "لا يوجد بيانات للطباعة")
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.print_table(printer)

    def print_table(self, printer):
        document = QTextDocument()
        html = """
        <html dir="rtl">
        <head>
            <style>
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid black; padding: 8px; text-align: right; }
                th { background-color: #f2f2f2; }
                h1 { text-align: center; }
            </style>
        </head>
        <body>
            <h1>التقرير اليومي للحضور</h1>
            <p>التاريخ: {}</p>
            <table>
                <tr>
        """.format(self.date_edit.date().toString("yyyy-MM-dd"))

        # Add headers and data
        headers = [self.report_table.horizontalHeaderItem(i).text() 
                  for i in range(self.report_table.columnCount())]
        html += "".join(f"<th>{header}</th>" for header in headers)
        html += "</tr>"

        for row in range(self.report_table.rowCount()):
            html += "<tr>"
            for col in range(self.report_table.columnCount()):
                item = self.report_table.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += """
            </table>
        </body>
        </html>
        """
        
        document.setHtml(html)
        document.print_(printer)

    def go_back_home(self):
        self.accept()  # This will close the dialog and return to main window

class MonthlyReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_table_behavior()
        self.reports = AttendanceReports()

    def init_ui(self):
        self.setWindowTitle("التقرير الشهري")
        self.setGeometry(200, 200, 1000, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QGroupBox {
                border: 2px solid #dcdde1;
                border-radius: 8px;
                margin-top: 1em;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTableWidget {
                border: 2px solid #dcdde1;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e8e8e8;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e8e8e8;
                border-right: 1px solid #e8e8e8;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #dcdde1;
                border-right: 1px solid #dcdde1;
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
            }
            QTableWidget::item:hover {
                background-color: #f0f6fc;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f9fa;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #95a5a6;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QDateEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                min-width: 120px;
            }
        """)

        layout = QVBoxLayout(self)

        # Back to Home button
        back_layout = QHBoxLayout()
        self.back_btn = QPushButton("العودة للرئيسية")
        self.back_btn.setIcon(QIcon("icons/home.png"))
        self.back_btn.setIconSize(QSize(24, 24))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
                text-align: center;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        self.back_btn.setToolTip("العودة للرئيسية")
        self.back_btn.clicked.connect(self.go_back_home)
        back_layout.addWidget(self.back_btn)
        back_layout.addStretch()
        layout.insertLayout(0, back_layout)

        # Title
        title = QLabel("التقرير الشهري للحضور ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        # Controls
        controls_layout = QHBoxLayout()
        
        month_label = QLabel("الشهر:")
        self.month_combo = QComboBox()
        self.month_combo.addItems([calendar.month_name[i] for i in range(1, 13)])
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        
        year_label = QLabel("السنة:")
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2020, 2100)
        self.year_spin.setValue(datetime.now().year)
        
        self.generate_btn = QPushButton("عرض التقرير")
        self.generate_btn.setIcon(QIcon("icons/report.png"))
        self.generate_btn.clicked.connect(self.generate_report)
        
        controls_layout.addWidget(month_label)
        controls_layout.addWidget(self.month_combo)
        controls_layout.addWidget(year_label)
        controls_layout.addWidget(self.year_spin)
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)

        # Report Table - Add total column
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(6)  # Changed to 6 columns
        self.report_table.setHorizontalHeaderLabels([
            "اسم الموظف", "أيام الحضور", "أيام الغياب",
            "أيام التأخير", "أيام الإجازة", "مجموع أيام الحضور"
        ])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.setAlternatingRowColors(True)
        layout.addWidget(self.report_table)

        # Print Button
        button_layout = QHBoxLayout()
        self.print_btn = QPushButton("طباعة التقرير")
        self.print_btn.setIcon(QIcon("icons/print.png"))
        self.print_btn.clicked.connect(self.print_report)
        button_layout.addStretch()
        button_layout.addWidget(self.print_btn)
        layout.addLayout(button_layout)

    def setup_table_behavior(self):
        """Setup enhanced table behavior"""
        # Make the entire row selectable
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        # Allow only one row to be selected at a time
        self.report_table.setSelectionMode(QTableWidget.SingleSelection)
        # Set row height
        self.report_table.verticalHeader().setDefaultSectionSize(50)
        # Hide vertical header (row numbers)
        self.report_table.verticalHeader().setVisible(False)
        # Make the table more responsive
        self.report_table.setMouseTracking(True)
        # Set text alignment for all columns
        self.report_table.setLayoutDirection(Qt.RightToLeft)
        # Set alternating row colors
        self.report_table.setAlternatingRowColors(True)

    def generate_report(self):
        year = self.year_spin.value()
        month = self.month_combo.currentIndex() + 1
        report_data = self.reports.generate_monthly_report(year, month)
        
        if report_data:
            self.report_table.setRowCount(0)
            for row_num, row in enumerate(report_data):
                self.report_table.insertRow(row_num)
                
                # Calculate total days - only present days
                total_days = row['present_days']  # Only count present days
                
                # Create items with proper values
                values = [
                    row['name'],
                    str(row['present_days']),
                    str(row['absent_days']),
                    str(row['late_days']),
                    str(row['vacation_days']),
                    str(total_days)  # Show only present days
                ]
                
                # Set items in table with center alignment
                for col, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.report_table.setItem(row_num, col, item)

    def print_report(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "تنبيه", "لا يوجد بيانات للطباعة")
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.print_table(printer)

    def print_table(self, printer):
        document = QTextDocument()
        html = """
        <html dir="rtl">
        <head>
            <style>
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid black; padding: 8px; text-align: right; }
                th { background-color: #f2f2f2; }
                h1 { text-align: center; }
            </style>
        </head>
        <body>
            <h1>التقرير الشهري للحضور والرواتب</h1>
            <p>الشهر: {} {}</p>
            <table>
                <tr>
        """.format(self.month_combo.currentText(), self.year_spin.value())

        # Add headers and data
        headers = [self.report_table.horizontalHeaderItem(i).text() 
                  for i in range(self.report_table.columnCount())]
        html += "".join(f"<th>{header}</th>" for header in headers)
        html += "</tr>"

        for row in range(self.report_table.rowCount()):
            html += "<tr>"
            for col in range(self.report_table.columnCount()):
                item = self.report_table.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"

        html += """
            </table>
        </body>
        </html>
        """
        
        document.setHtml(html)
        document.print_(printer)

    def go_back_home(self):
        self.accept()  # This will close the dialog and return to main window 