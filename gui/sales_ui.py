from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, 
                           QTableWidgetItem, QMessageBox, QComboBox,
                           QFrame, QHeaderView, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from database.models import Part, Sale
from database.db_setup import Session
from datetime import datetime

class SalesUI(QWidget):
    sale_completed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.init_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: Arial;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                min-width: 200px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#addButton {
                background-color: #2ecc71;
            }
            QPushButton#addButton:hover {
                background-color: #27ae60;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QFrame#searchFrame, QFrame#saleFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
        """)

    def init_ui(self):
        # إعداد النافذة الرئيسية
        self.setWindowTitle("إدارة المبيعات")
        self.setGeometry(100, 100, 1000, 700)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # إطار البحث
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout(search_frame)
        
        search_label = QLabel("بحث عن القطعة:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ادخل اسم القطعة أو رقمها")
        search_button = QPushButton("بحث")
        search_button.setIcon(QIcon("icons/search.png"))
        search_button.setIconSize(QSize(20, 20))
        search_button.clicked.connect(self.search_parts)
        
        search_layout.addWidget(search_button)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_label)

        # جدول القطع
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(6)
        headers = ["السعر", "الكمية", "سعر التكلفة", "النوع", "الاسم", "رقم القطعة"]
        self.parts_table.setHorizontalHeaderLabels(headers)
        self.parts_table.setLayoutDirection(Qt.RightToLeft)
        
        # تنسيق الجدول
        self.parts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.verticalHeader().setVisible(False)

        # إطار إضافة المبيعات
        sale_frame = QFrame()
        sale_frame.setObjectName("saleFrame")
        sale_layout = QHBoxLayout(sale_frame)
        
        # مدخلات البيع
        quantity_label = QLabel("الكمية:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("أدخل الكمية")
        
        price_label = QLabel("سعر البيع:")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("أدخل سعر البيع")
        
        add_sale_button = QPushButton("إضافة عملية بيع")
        add_sale_button.setObjectName("addButton")
        add_sale_button.setIcon(QIcon("icons/add.png"))
        add_sale_button.setIconSize(QSize(20, 20))
        add_sale_button.clicked.connect(self.add_sale)

        # إضافة العناصر إلى تخطيط البيع
        sale_layout.addWidget(add_sale_button)
        sale_layout.addWidget(self.price_input)
        sale_layout.addWidget(price_label)
        sale_layout.addWidget(self.quantity_input)
        sale_layout.addWidget(quantity_label)

        # إضافة كل شيء إلى التخطيط الرئيسي
        main_layout.addWidget(search_frame)
        main_layout.addWidget(self.parts_table)
        main_layout.addWidget(sale_frame)

        self.setLayout(main_layout)

    def search_parts(self):
        search_text = self.search_input.text()
        
        query = self.session.query(Part)
        if search_text:
            query = query.filter(
                (Part.name.ilike(f'%{search_text}%')) |
                (Part.part_number.ilike(f'%{search_text}%'))
            )
        
        parts = query.all()
        self.update_parts_table(parts)

    def update_parts_table(self, parts):
        self.parts_table.setRowCount(len(parts))
        
        for row, part in enumerate(parts):
            items = [
                str(part.selling_price),
                str(part.quantity),
                str(part.cost_price),
                part.type,
                part.name,
                part.part_number
            ]
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignCenter)
                self.parts_table.setItem(row, col, table_item)

    def add_sale(self):
        current_row = self.parts_table.currentRow()
        if current_row < 0:
            self.show_message("تنبيه", "الرجاء اختيار قطعة من الجدول", QMessageBox.Warning)
            return

        try:
            quantity = int(self.quantity_input.text())
            selling_price = float(self.price_input.text())
        except ValueError:
            self.show_message("خطأ", "الرجاء إدخال أرقام صحيحة", QMessageBox.Critical)
            return

        part_number = self.parts_table.item(current_row, 5).text()
        part = self.session.query(Part).filter_by(part_number=part_number).first()

        if not part:
            self.show_message("خطأ", "لم يتم العثور على القطعة", QMessageBox.Critical)
            return

        if quantity > part.quantity:
            self.show_message("خطأ", "الكمية المطلوبة غير متوفرة في المخزون", QMessageBox.Critical)
            return

        # إنشاء عملية البيع
        sale = Sale(
            part_id=part.id,
            quantity=quantity,
            selling_price=selling_price,
            sale_date=datetime.now(),
            profit=(selling_price - part.cost_price) * quantity
        )

        # تحديث الكمية
        part.quantity -= quantity

        try:
            self.session.add(sale)
            self.session.commit()
            self.search_parts()  # تحديث الجدول
            self.clear_inputs()
            self.show_message("نجاح", "تم تسجيل عملية البيع بنجاح", QMessageBox.Information)
            self.sale_completed.emit()
        except Exception as e:
            self.session.rollback()
            self.show_message("خطأ", f"حدث خطأ أثناء تسجيل البيع: {str(e)}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()

    def clear_inputs(self):
        self.quantity_input.clear()
        self.price_input.clear()

    def closeEvent(self, event):
        self.session.close()
        super().closeEvent(event) 