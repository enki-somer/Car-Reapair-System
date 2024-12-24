from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QComboBox, QSpinBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import sqlite3
from datetime import datetime

class WorkerManagementUI(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.db_path = "database/workers.db"
        self.current_worker_id = None
        self.refresh_table()  # Load initial data

    def init_ui(self):
        self.setWindowTitle("إدارة الموظفين")
        self.setGeometry(150, 150, 800, 600)
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
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QSpinBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                border: none;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                min-width: 200px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

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
        main_layout.insertLayout(0, back_layout)

        # Title
        title_label = QLabel("نظام إدارة الموظفين")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Form layout for worker details
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم الموظف")
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("أدخل رقم الهاتف")
        
        self.salary_input = QSpinBox()
        self.salary_input.setRange(0, 1000000)
        self.salary_input.setSingleStep(100)
        self.salary_input.setButtonSymbols(QSpinBox.NoButtons)  # Hide up/down buttons
        self.salary_input.setAlignment(Qt.AlignCenter)
        
        self.status_input = QComboBox()
        self.status_input.addItems(["نشط", "غير نشط", "إجازة"])

        # Add form fields with Arabic labels
        form_layout.addRow("اسم العامل:", self.name_input)
        form_layout.addRow("رقم الهاتف:", self.phone_input)
        form_layout.addRow("الراتب:", self.salary_input)
        form_layout.addRow("الحالة:", self.status_input)

        main_layout.addLayout(form_layout)

        # Table to display workers
        self.workers_table = QTableWidget()
        self.workers_table.setColumnCount(4)
        self.workers_table.setHorizontalHeaderLabels([
            "اسم الموظف", "رقم الهاتف", "الراتب", "الحالة"
        ])
        self.workers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.workers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.workers_table.setSelectionMode(QTableWidget.SingleSelection)
        self.workers_table.setLayoutDirection(Qt.RightToLeft)
        self.workers_table.verticalHeader().setVisible(True)
        self.workers_table.setAlternatingRowColors(True)
        self.workers_table.verticalHeader().setDefaultSectionSize(50)
        self.workers_table.itemClicked.connect(self.load_worker_data)
        main_layout.addWidget(self.workers_table)

        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة")
        self.add_button.setIcon(QIcon("icons/add.png"))  # Assuming you have icons
        
        self.update_button = QPushButton("تحديث")
        self.update_button.setIcon(QIcon("icons/update.png"))
        
        self.delete_button = QPushButton("حذف")
        self.delete_button.setIcon(QIcon("icons/delete.png"))
        
        self.clear_button = QPushButton("مسح الحقول")
        self.clear_button.setIcon(QIcon("icons/clear.png"))

        self.add_button.clicked.connect(self.add_worker)
        self.update_button.clicked.connect(self.update_worker)
        self.delete_button.clicked.connect(self.delete_worker)
        self.clear_button.clicked.connect(self.clear_fields)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Add style for vertical header (row numbers)
        self.workers_table.setStyleSheet(self.workers_table.styleSheet() + """
            QHeaderView::section:vertical {
                background-color: #f8f9fa;
                padding: 5px;
                border: none;
                border-right: 2px solid #dcdde1;
                font-weight: bold;
                color: #2c3e50;
                font-size: 12px;
            }
        """)

    def get_db_connection(self):
        """Create and return a database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ في قاعدة البيانات", f"فشل الاتصال بقاعدة البيانات: {str(e)}")
            return None

    def refresh_table(self):
        """Refresh the workers table with current database data"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return

            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, phone, salary, status, created_at, updated_at 
                FROM workers 
                ORDER BY name
            """)
            
            self.workers_table.setRowCount(0)
            
            for row_num, row in enumerate(cursor.fetchall()):
                self.workers_table.insertRow(row_num)
                
                # Create items with proper values and alignment (excluding ID)
                items = [
                    QTableWidgetItem(row['name']),
                    QTableWidgetItem(row['phone']),
                    QTableWidgetItem(self.format_salary(row['salary'])),  # Format salary
                    QTableWidgetItem(row['status'])
                ]
                
                # Set alignment for each item
                for col, item in enumerate(items):
                    item.setTextAlignment(Qt.AlignCenter)
                    self.workers_table.setItem(row_num, col, item)
                    
                # Store the ID as hidden data in the first column
                self.workers_table.item(row_num, 0).setData(Qt.UserRole, row['id'])
                
                # Set the row number
                self.workers_table.setVerticalHeaderItem(row_num, 
                    QTableWidgetItem(str(row_num + 1)))

            conn.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحديث البيانات: {str(e)}")

    def add_worker(self):
        if not self.validate_inputs():
            return
        
        try:
            conn = self.get_db_connection()
            if not conn:
                return

            cursor = conn.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                INSERT INTO workers (name, phone, salary, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.name_input.text().strip(),
                self.phone_input.text().strip(),
                self.salary_input.value(),
                self.status_input.currentText(),
                current_time,
                current_time
            ))
            
            conn.commit()
            conn.close()
            
            self.refresh_table()
            self.clear_fields()
            QMessageBox.information(self, "نجاح", "تم إضافة الموظف بنجاح")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إضافة الموظف: {str(e)}")

    def update_worker(self):
        if not self.validate_inputs() or not self.current_worker_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد الموظف المراد تحديثه")
            return
        
        try:
            conn = self.get_db_connection()
            if not conn:
                return

            cursor = conn.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                UPDATE workers 
                SET name = ?, phone = ?, salary = ?, status = ?, updated_at = ?
                WHERE id = ?
            """, (
                self.name_input.text().strip(),
                self.phone_input.text().strip(),
                self.salary_input.value(),
                self.status_input.currentText(),
                current_time,
                self.current_worker_id
            ))
            
            conn.commit()
            conn.close()
            
            self.refresh_table()
            QMessageBox.information(self, "نجاح", "تم تحديث بيانات الموظف بنجاح")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحديث البيانات: {str(e)}")

    def delete_worker(self):
        if not self.current_worker_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد الموظف المراد حذفه")
            return

        reply = QMessageBox.question(self, "تأكيد الحذف", 
                                   "هل أنت متأكد من حذف هذا الموظف؟",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.get_db_connection()
                if not conn:
                    return

                cursor = conn.cursor()
                cursor.execute("DELETE FROM workers WHERE id = ?", (self.current_worker_id,))
                conn.commit()
                conn.close()
                
                self.refresh_table()
                self.clear_fields()
                self.current_worker_id = None
                QMessageBox.information(self, "نجاح", "تم حذف الموظف بنجاح")
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حذف الموظف: {str(e)}")

    def load_worker_data(self, item):
        row = item.row()
        self.current_worker_id = self.workers_table.item(row, 0).data(Qt.UserRole)
        self.name_input.setText(self.workers_table.item(row, 0).text())
        self.phone_input.setText(self.workers_table.item(row, 1).text())
        # Remove commas before converting to integer
        salary_text = self.workers_table.item(row, 2).text().replace(',', '')
        self.salary_input.setValue(int(salary_text))
        self.status_input.setCurrentText(self.workers_table.item(row, 3).text())

    def clear_fields(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.salary_input.setValue(0)
        self.status_input.setCurrentIndex(0)

    def validate_inputs(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال اسم الموظف")
            return False
        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال رقم الهاتف")
            return False
        return True

    def format_salary(self, amount):
        """Format salary with commas for better readability"""
        return "{:,}".format(amount)

    def go_back_home(self):
        self.accept()  # This will close the dialog and return to main window