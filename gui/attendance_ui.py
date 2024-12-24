from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QDateEdit, QMessageBox, QHeaderView,
    QGroupBox, QSpinBox, QWidget, QFrame, QFormLayout, QLineEdit, QCompleter
)
from PyQt5.QtCore import Qt, QDate, QStringListModel, QSize
from PyQt5.QtGui import QFont, QIcon
import sqlite3
from datetime import datetime
from app.reports import AttendanceReports
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
import calendar
from .report_windows import DailyReportWindow, MonthlyReportWindow

class AttendanceUI(QDialog):
    def __init__(self):
        super().__init__()
        self.db_path = "database/workers.db"
        self.init_ui()
        self.setup_table_behavior()
        self.load_workers()
        self.refresh_attendance()

    def init_ui(self):
        self.setWindowTitle("نظام تسجيل الحضور والانصراف")
        self.setGeometry(100, 100, 1200, 800)
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
            QGroupBox::title {
                color: #2f3640;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2475a8;
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
                text-align: center;
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
            QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                min-width: 150px;
            }
            QLabel {
                color: #2f3640;
                font-size: 13px;
            }
            #titleLabel {
                font-size: 24px;
                color: #2f3640;
                padding: 10px;
            }
            QTableWidget::item:hover {
                background-color: #ebf5fb;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QTableWidget {
                selection-background-color: #3498db;
                selection-color: white;
                gridline-color: #f1f2f6;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f2f6;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

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
        title_label = QLabel("نظام تسجيل الحضور والانصراف")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Attendance Control Group
        attendance_group = QGroupBox("تسجيل الحضور والانصراف")
        attendance_layout = QVBoxLayout()

        # Top controls in horizontal layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        # Worker selection with label
        worker_layout = QHBoxLayout()
        worker_label = QLabel("اختر العامل :")
        worker_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.worker_combo = QComboBox()
        self.worker_combo.setMinimumWidth(200)
        worker_layout.addWidget(self.worker_combo)
        worker_layout.addWidget(worker_label)
        controls_layout.addLayout(worker_layout)

        # Search box for workers with auto-completion
        search_layout = QHBoxLayout()
        search_label = QLabel("بحث عن عامل :")
        self.search_input = QLineEdit()
        self.search_input.setLayoutDirection(Qt.RightToLeft)  # Set RTL for cursor
        self.search_input.setAlignment(Qt.AlignRight)  # Align text to right
        self.search_input.setPlaceholderText("اكتب اسم العامل للبحث...")
        
        # Setup auto-completion
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(self.completer)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_label)
        controls_layout.addLayout(search_layout)

        # Add style for search input
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        # Date selection with label
        date_layout = QHBoxLayout()
        date_label = QLabel("التاريخ :")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.refresh_attendance)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(date_label)
        controls_layout.addLayout(date_layout)

        # Status selection with label
        status_layout = QHBoxLayout()
        status_label = QLabel("الحالة :")
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["حاضر", "غائب", "متأخر", "إجازة"])
        status_layout.addWidget(self.status_combo)
        status_layout.addWidget(status_label)
        controls_layout.addLayout(status_layout)

        attendance_layout.addLayout(controls_layout)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.mark_attendance_btn = QPushButton("تسجيل الحضور")
        self.mark_attendance_btn.setIcon(QIcon("icons/check-in.png"))
        self.mark_leave_btn = QPushButton("تسجيل الانصراف")
        self.mark_leave_btn.setIcon(QIcon("icons/check-out.png"))
        self.edit_attendance_btn = QPushButton("تعديل الحضور")
        self.edit_attendance_btn.setIcon(QIcon("icons/edit.png"))
        self.refresh_btn = QPushButton("تحديث")
        self.refresh_btn.setIcon(QIcon("icons/refresh.png"))

        self.mark_attendance_btn.clicked.connect(self.mark_attendance)
        self.mark_leave_btn.clicked.connect(self.mark_leave)
        self.edit_attendance_btn.clicked.connect(self.edit_attendance)
        self.refresh_btn.clicked.connect(self.refresh_attendance)

        button_layout.addWidget(self.mark_attendance_btn)
        button_layout.addWidget(self.mark_leave_btn)
        button_layout.addWidget(self.edit_attendance_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()

        attendance_layout.addLayout(button_layout)
        attendance_group.setLayout(attendance_layout)
        main_layout.addWidget(attendance_group)

        # Attendance Table Group
        table_group = QGroupBox("سجل الحضور اليومي")
        table_layout = QVBoxLayout()
        
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(5)
        self.attendance_table.setHorizontalHeaderLabels([
            "اسم العامل", "التاريخ", "وقت الحضور", "وقت الانصراف", "الحالة"
        ])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setAlternatingRowColors(True)
        self.attendance_table.setLayoutDirection(Qt.RightToLeft)
        table_layout.addWidget(self.attendance_table)
        
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        # Reports Group
        reports_group = QGroupBox("التقارير")
        reports_layout = QHBoxLayout()

        self.daily_report_btn = QPushButton("التقرير الومي")
        self.daily_report_btn.setIcon(QIcon("icons/daily-report.png"))
        self.monthly_report_btn = QPushButton("التقرير الشهري")
        self.monthly_report_btn.setIcon(QIcon("icons/monthly-report.png"))

        self.daily_report_btn.clicked.connect(self.show_daily_report)
        self.monthly_report_btn.clicked.connect(self.show_monthly_report)

        reports_layout.addWidget(self.daily_report_btn)
        reports_layout.addWidget(self.monthly_report_btn)

        reports_group.setLayout(reports_layout)
        main_layout.addWidget(reports_group)

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"فشل الاتصال بقاعدة البيانات: {str(e)}")
            return None

    def load_workers(self):
        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, phone 
                FROM workers 
                WHERE status = 'نشط' 
                ORDER BY name
            """)
            workers = cursor.fetchall()
            
            self.worker_combo.clear()
            self.workers_data = {}
            worker_names = []  # List for completer
            
            # Add a placeholder
            self.worker_combo.addItem("-- اختر عامل --")
            
            for worker in workers:
                worker_name = worker['name']
                self.worker_combo.addItem(worker_name)
                self.workers_data[worker_name] = {
                    'id': worker['id'],
                    'phone': worker['phone']
                }
                worker_names.append(worker_name)
            
            # Update completer with current worker names
            self.completer.setModel(QStringListModel(worker_names))
            
            conn.close()
            
            # Setup combo box behavior
            self.worker_combo.setMaxVisibleItems(10)
            self.worker_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات العمال: {str(e)}")

    def refresh_attendance(self):
        """Refresh the attendance table with current day's data"""
        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            current_date = self.date_edit.date().toPyDate()
            
            cursor.execute("""
                SELECT 
                    a.id,
                    w.name,
                    a.date,
                    a.time_in,
                    a.time_out,
                    a.status
                FROM attendance a
                JOIN workers w ON a.worker_id = w.id
                WHERE a.date = ?
                ORDER BY w.name
            """, (current_date,))
            
            self.attendance_table.setRowCount(0)
            
            for row_num, row in enumerate(cursor.fetchall()):
                self.attendance_table.insertRow(row_num)
                
                # Create and set items with alignment
                name_item = QTableWidgetItem(row['name'])
                date_item = QTableWidgetItem(str(row['date']))
                time_in_item = QTableWidgetItem(str(row['time_in'] or ''))
                time_out_item = QTableWidgetItem(str(row['time_out'] or ''))
                status_item = QTableWidgetItem(row['status'])
                
                # Set alignment for each item
                for item in [name_item, date_item, time_in_item, time_out_item, status_item]:
                    item.setTextAlignment(Qt.AlignCenter)
                
                # Set items in table
                self.attendance_table.setItem(row_num, 0, name_item)
                self.attendance_table.setItem(row_num, 1, date_item)
                self.attendance_table.setItem(row_num, 2, time_in_item)
                self.attendance_table.setItem(row_num, 3, time_out_item)
                self.attendance_table.setItem(row_num, 4, status_item)
                
                # Store the ID as item data
                name_item.setData(Qt.UserRole, row['id'])
            
            conn.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحديث جدول الحضور: {str(e)}")

    def mark_attendance(self):
        """تسجيل حضور موظف"""
        worker_name = self.worker_combo.currentText()
        if worker_name == "-- اختر عامل --":
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار عامل")
            return

        worker_id = self.workers_data[worker_name]['id']  # Get worker ID
        current_date = self.date_edit.date().toPyDate()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = self.status_combo.currentText()

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            # Check if attendance record already exists for this worker on this date
            cursor.execute("""
                SELECT id FROM attendance 
                WHERE worker_id = ? AND date = ?
            """, (worker_id, current_date))
            
            if cursor.fetchone():
                QMessageBox.warning(self, "تنبيه", "تم تسجيل حضور هذا العامل مسبقاً لهذا اليوم")
                return

            # Insert new attendance record
            cursor.execute("""
                INSERT INTO attendance (worker_id, date, time_in, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (worker_id, current_date, current_time, status, current_time))
            
            conn.commit()
            conn.close()
            
            self.refresh_attendance()
            QMessageBox.information(self, "نجاح", "تم تسجيل الحضور بنجاح")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تسجيل الحضور: {str(e)}")
            if conn:
                conn.rollback()

    def mark_leave(self):
        selected_items = self.attendance_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار سجل حضور")
            return

        row = selected_items[0].row()
        attendance_id = self.attendance_table.item(row, 0).data(Qt.UserRole)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance 
                SET time_out = ?
                WHERE id = ?
            """, (current_time, attendance_id))
            
            conn.commit()
            conn.close()
            
            self.refresh_attendance()
            QMessageBox.information(self, "نجاح", "تم تسجيل الانصراف بنجاح")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تسجيل الانصراف: {str(e)}")

    def show_daily_report(self):
        daily_report = DailyReportWindow()
        daily_report.exec_()

    def show_monthly_report(self):
        monthly_report = MonthlyReportWindow()
        monthly_report.exec_()

    def edit_attendance(self):
        selected_items = self.attendance_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار سجل حضور للتعديل")
            return

        row = selected_items[0].row()
        attendance_id = self.attendance_table.item(row, 0).data(Qt.UserRole)
        worker_name = self.attendance_table.item(row, 0).text()

        # Create edit dialog
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("تعديل سجل الحضور")
        edit_dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(edit_dialog)

        # Preview label
        preview_label = QLabel("معاينة التغييرات:")
        preview_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        layout.addWidget(preview_label)

        # Preview table
        preview_table = QTableWidget()
        preview_table.setColumnCount(5)
        preview_table.setRowCount(1)
        preview_table.setHorizontalHeaderLabels([
            "اسم العامل", "التاريخ", "وقت الحضور", "وقت الانصراف", "الحالة"
        ])
        preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        preview_table.setAlternatingRowColors(True)
        preview_table.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(preview_table)

        # Form layout for editing
        form_layout = QFormLayout()

        # Status selection
        status_combo = QComboBox()
        status_combo.addItems(["حاضر", "غائب", "متأخر", "إجازة"])
        current_status = self.attendance_table.item(row, 4).text()
        status_combo.setCurrentText(current_status)
        form_layout.addRow("الحالة:", status_combo)

        # Time in
        time_in = self.attendance_table.item(row, 2).text()
        time_in_edit = QLineEdit(time_in)
        form_layout.addRow("وقت الحضور:", time_in_edit)

        # Time out
        time_out = self.attendance_table.item(row, 3).text()
        time_out_edit = QLineEdit(time_out)
        form_layout.addRow("وقت الانصراف:", time_out_edit)

        layout.addLayout(form_layout)

        # Update preview function
        def update_preview():
            preview_table.setItem(0, 0, QTableWidgetItem(worker_name))
            preview_table.setItem(0, 1, QTableWidgetItem(self.attendance_table.item(row, 1).text()))
            preview_table.setItem(0, 2, QTableWidgetItem(time_in_edit.text()))
            preview_table.setItem(0, 3, QTableWidgetItem(time_out_edit.text()))
            preview_table.setItem(0, 4, QTableWidgetItem(status_combo.currentText()))
            
            # Center align all items
            for col in range(5):
                item = preview_table.item(0, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

        # Connect changes to preview update
        status_combo.currentTextChanged.connect(update_preview)
        time_in_edit.textChanged.connect(update_preview)
        time_out_edit.textChanged.connect(update_preview)

        # Initial preview
        update_preview()

        # Buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("حفظ التغييرات")
        delete_btn = QPushButton("حذف السجل")
        cancel_btn = QPushButton("إلغاء")

        save_btn.clicked.connect(lambda: self.save_attendance_changes(
            edit_dialog,
            attendance_id,
            status_combo.currentText(),
            time_in_edit.text(),
            time_out_edit.text()
        ))
        delete_btn.clicked.connect(lambda: self.delete_attendance_record(
            edit_dialog,
            attendance_id
        ))
        cancel_btn.clicked.connect(edit_dialog.reject)

        button_box.addWidget(save_btn)
        button_box.addWidget(delete_btn)
        button_box.addWidget(cancel_btn)

        layout.addLayout(button_box)

        # Show dialog
        edit_dialog.setMinimumWidth(600)
        edit_dialog.setMinimumHeight(400)
        edit_dialog.exec_()

    def save_attendance_changes(self, dialog, attendance_id, status, time_in, time_out):
        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance 
                SET status = ?,
                    time_in = ?,
                    time_out = ?
                WHERE id = ?
            """, (status, time_in, time_out, attendance_id))
            
            conn.commit()
            conn.close()
            
            self.refresh_attendance()
           # QMessageBox.information(self, "نجاح", "تم تحديث سجل الحضور بنجاح")
            dialog.accept()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحديث سجل الحضور: {str(e)}")

    def delete_attendance_record(self, dialog, attendance_id):
        reply = QMessageBox.question(
            self, 
            "تأكيد الحذف",
            "هل أنت متأكد من حذف سجل الحضور هذا؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            conn = self.get_db_connection()
            if not conn:
                return

            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
                conn.commit()
                conn.close()
                
                self.refresh_attendance()
                QMessageBox.information(self, "نجاح", "تم حذف سجل الحضور بنجاح")
                dialog.accept()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في حذف سجل الحضور: {str(e)}")

    def filter_workers(self, text):
        """Filter workers in combo box based on search text"""
        if not text:  # If search is empty, show all workers
            self.worker_combo.clear()
            self.worker_combo.addItem("-- اختر عامل --")
            for worker_name in self.workers_data.keys():
                self.worker_combo.addItem(worker_name)
            return

        self.worker_combo.clear()
        search_text = text.lower()
        
        # Add matching workers
        for worker_name in self.workers_data.keys():
            if search_text in worker_name.lower():
                self.worker_combo.addItem(worker_name)
        
        # If we have exactly one match and it's complete, select it
        if self.worker_combo.count() == 1 and \
           self.worker_combo.itemText(0).lower().startswith(search_text):
            self.worker_combo.setCurrentIndex(0)

    def setup_table_behavior(self):
        """Setup enhanced table behavior"""
        # Make the entire row selectable
        self.attendance_table.setSelectionBehavior(QTableWidget.SelectRows)
        # Allow only one row to be selected at a time
        self.attendance_table.setSelectionMode(QTableWidget.SingleSelection)
        # Set row height
        self.attendance_table.verticalHeader().setDefaultSectionSize(50)
        # Hide vertical header (row numbers)
        self.attendance_table.verticalHeader().setVisible(False)
        # Make the table more responsive
        self.attendance_table.setMouseTracking(True)
        # Enable sorting
        self.attendance_table.setSortingEnabled(True)
        # Double click to edit
        self.attendance_table.doubleClicked.connect(self.edit_attendance)
        # Set text alignment for all columns
        self.attendance_table.setLayoutDirection(Qt.RightToLeft)
        # Set alternating row colors
        self.attendance_table.setAlternatingRowColors(True)
        # Set the alternating row color
        self.attendance_table.setStyleSheet(self.attendance_table.styleSheet() + """
            QTableWidget {
                alternate-background-color: #f8f9fa;
            }
        """)

    def go_back_home(self):
        self.accept()  # This will close the dialog and return to main window
