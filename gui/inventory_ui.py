from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, 
                           QTableWidgetItem, QMessageBox, QComboBox,
                           QFrame, QHeaderView, QSpacerItem, QSizePolicy,
                           QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from database.models import Part
from database.db_setup import Session
from datetime import datetime
from sqlalchemy import func

class AddPartDialog(QDialog):
    def __init__(self, parent=None, part=None):
        super().__init__(parent)
        self.part = part
        self.init_ui()
        if part:
            self.setWindowTitle("تعديل بيانات القطعة")
            self.fill_form_data()

    def init_ui(self):
        self.setMinimumWidth(400)
        layout = QFormLayout()
        layout.setSpacing(15)
        
        # إنشاء حقول الإدخال
        self.part_number = QLineEdit()
        self.name = QLineEdit()
        self.type = QComboBox()
        self.type.addItems([
            "محرك", "فرامل", "تعليق", "كهرباء", "هيكل", "إطارات", 
            "زيوت", "فلاتر", "أخرى"
        ])
        self.quantity = QLineEdit()
        self.cost_price = QLineEdit()
        self.selling_price = QLineEdit()
        
        # إضافة التلميحات
        self.part_number.setPlaceholderText("مثال: P12345")
        self.name.setPlaceholderText("اسم القطعة")
        self.quantity.setPlaceholderText("الكمية المتوفرة")
        self.cost_price.setPlaceholderText("سعر الشراء")
        self.selling_price.setPlaceholderText("سعر البيع")
        
        # تعطيل تعديل رقم القطعة في حالة التعديل
        if self.part:
            self.part_number.setEnabled(False)
        
        # إضافة الحقول إلى النموذج
        layout.addRow("رقم القطعة:", self.part_number)
        layout.addRow("اسم القطعة:", self.name)
        layout.addRow("النوع:", self.type)
        layout.addRow("الكمية:", self.quantity)
        layout.addRow("سعر التكلفة:", self.cost_price)
        layout.addRow("سعر البيع:", self.selling_price)
        
        # أزرار الحفظ والإلغاء
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        save_btn.setObjectName("addButton")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow("", btn_layout)
        
        self.setLayout(layout)

    def fill_form_data(self):
        """تعبئة البيانات الحالية للقطعة"""
        self.part_number.setText(self.part.part_number)
        self.name.setText(self.part.name)
        self.type.setCurrentText(self.part.type)
        self.quantity.setText(str(self.part.quantity))
        self.cost_price.setText(str(self.part.cost_price))
        self.selling_price.setText(str(self.part.selling_price))

    def validate_and_accept(self):
        """التحقق من صحة البيانات قبل الحفظ"""
        try:
            # التحقق من تعبئة الحقول الإلزامية
            if not all([self.part_number.text(), self.name.text()]):
                raise ValueError("جميع الحقول مطلوبة")

            # التحقق من صحة الأرقام
            quantity = int(self.quantity.text())
            cost_price = float(self.cost_price.text())
            selling_price = float(self.selling_price.text())

            if quantity < 0:
                raise ValueError("الكمية يجب أن تكون أكبر من أو تساوي صفر")
            if cost_price <= 0:
                raise ValueError("سعر التكلفة يجب أن يكون أكبر من صفر")
            if selling_price <= 0:
                raise ValueError("سعر البيع يجب أن يكون أكبر من صفر")
            if selling_price < cost_price:
                raise ValueError("سعر البيع يجب أن يكون أكبر من سعر التكلفة")

            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "خطأ في البيانات", str(e))

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.init_ui()
        self.load_parts()
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
                font-size: 18px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#deleteButton {
                background-color: #e74c3c;
            }
            QPushButton#deleteButton:hover {
                background-color: #c0392b;
            }
            QPushButton#addButton {
                background-color: #2ecc71;
            }
            QPushButton#addButton:hover {
                background-color: #27ae60;
            }
            QPushButton#refreshButton {
                background-color: #f39c12;
            }
            QPushButton#refreshButton:hover {
                background-color: #f39c12;
            }
            QPushButton#backButton {
                background-color: #95a5a6;
            }
            QPushButton#backButton:hover {
                background-color: #7f8c8d;
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
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QFrame#toolFrame, QFrame#statsFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
            QLabel#statsLabel {
                color: #2c3e50;
                font-size: 16px;
            }
            QLabel#valueLabel {
                color: #3498db;
                font-size: 18px;
                font-weight: bold;
            }
        """)

    def init_ui(self):
        self.setWindowTitle("إدارة المخزون")
        self.setGeometry(100, 100, 1200, 800)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # إطار الأدوات العلوي
        tool_frame = QFrame()
        tool_frame.setObjectName("toolFrame")
        tool_layout = QHBoxLayout(tool_frame)

        # زر العودة للرئيسية
        back_button = QPushButton("العودة للرئيسية")
        back_button.setIcon(QIcon("icons/home.png"))
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.close)

        # حقل البحث مع أيقونة
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        search_label = QLabel()
        search_label.setPixmap(QIcon("icons/search.png").pixmap(20, 20))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن قطعة...")
        self.search_input.textChanged.connect(self.search_parts)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # أزرار الإدارة
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)

        refresh_button = QPushButton("تحديث")
        refresh_button.setIcon(QIcon("icons/refresh.png"))
        refresh_button.setObjectName("refreshButton")
        refresh_button.clicked.connect(self.refresh_inventory)

        add_button = QPushButton("إضافة قطعة")
        add_button.setObjectName("addButton")
        add_button.setIcon(QIcon("icons/add.png"))
        add_button.clicked.connect(self.add_part)

        delete_button = QPushButton("حذف قطعة")
        delete_button.setObjectName("deleteButton")
        delete_button.setIcon(QIcon("icons/delete.png"))
        delete_button.clicked.connect(self.delete_part)

        button_layout.addWidget(refresh_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        # إضافة كل شيء إلى شريط الأدوات
        tool_layout.addWidget(back_button)
        tool_layout.addWidget(search_frame)
        tool_layout.addStretch()
        tool_layout.addWidget(button_frame)

        # إطار الإحصائيات
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_layout = QHBoxLayout(stats_frame)

        # إجمالي القطع
        total_parts = QVBoxLayout()
        total_parts_label = QLabel("إجمالي القطع")
        total_parts_label.setObjectName("statsLabel")
        self.total_parts_value = QLabel("0")
        self.total_parts_value.setObjectName("valueLabel")
        total_parts.addWidget(total_parts_label)
        total_parts.addWidget(self.total_parts_value)

        # القطع منخفضة المخزون
        low_stock = QVBoxLayout()
        low_stock_label = QLabel("منخفض المخزون")
        low_stock_label.setObjectName("statsLabel")
        self.low_stock_value = QLabel("0")
        self.low_stock_value.setObjectName("valueLabel")
        low_stock.addWidget(low_stock_label)
        low_stock.addWidget(self.low_stock_value)

        # القيمة ��لإجمالية
        total_value = QVBoxLayout()
        total_value_label = QLabel("القيمة الإجمالية")
        total_value_label.setObjectName("statsLabel")
        self.total_value_amount = QLabel("0 دينار")
        self.total_value_amount.setObjectName("valueLabel")
        total_value.addWidget(total_value_label)
        total_value.addWidget(self.total_value_amount)

        stats_layout.addLayout(total_parts)
        stats_layout.addLayout(low_stock)
        stats_layout.addLayout(total_value)

        # جدول القطع
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(7)
        headers = ["رقم القطعة", "الاسم", "النوع", "الكمية", "سعر التكلفة", "سعر البيع", "آخر تحديث"]
        self.parts_table.setHorizontalHeaderLabels(headers)
        self.parts_table.setLayoutDirection(Qt.RightToLeft)
        
        # تنسيق الجدول
        self.parts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.verticalHeader().setVisible(False)
        self.parts_table.itemDoubleClicked.connect(self.edit_part)

        # إضافة كل شيء إلى التخطيط الرئيسي
        main_layout.addWidget(tool_frame)
        main_layout.addWidget(stats_frame)
        main_layout.addWidget(self.parts_table)
        
        self.setLayout(main_layout)

    def update_stats(self):
        """تحديث الإحصائيات"""
        try:
            # إجمالي أنواع القطع (عدد القطع المختلفة)
            unique_parts = self.session.query(Part).count()
            
            # إجمالي الكمية (مجموع كميات جميع القطع)
            total_quantity = self.session.query(func.sum(Part.quantity)).scalar() or 0
            
            
            # تنسيق العرض بشكل أوضح
            if unique_parts == 0:
                self.total_parts_value.setText("لا توجد قطع")
                self.low_stock_value.setText("-")
                self.total_value_amount.setText("-")
            else:
                self.total_parts_value.setText(f" نوع - {total_quantity} قطعة")
                
                # القطع منخفضة المخزون
                low_stock = self.session.query(Part).filter(Part.quantity <= 5).count()
                self.low_stock_value.setText(str(low_stock) if low_stock > 0 else "لا يوجد")

            # القيمة الإجمالية
            total_value = sum(part.cost_price * part.quantity 
                            for part in self.session.query(Part).all())
            self.total_value_amount.setText(f"{total_value:,.2f} دينار")

        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ أثناء تحديث الإحصائيات: {str(e)}", QMessageBox.Critical)

    def load_parts(self):
        """تحميل جميع القطع من قاعدة البيانات"""
        parts = self.session.query(Part).all()
        self.update_table(parts)
        self.update_stats()

    def refresh_inventory(self):
        """تحديث عرض المخزون"""
        try:
            self.session.expire_all()
            self.load_parts()
            self.show_message("نجاح", "تم تحديث المخزون بنجاح", QMessageBox.Information)
        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ أثناء تحديث المخزون: {str(e)}", QMessageBox.Critical)

    def update_table(self, parts):
        """تحديث جدول القطع"""
        self.parts_table.setRowCount(len(parts))
        for row, part in enumerate(parts):
            items = [
                part.part_number,
                part.name,
                part.type,
                str(part.quantity),
                str(part.cost_price),
                str(part.selling_price),
                datetime.now().strftime("%Y-%m-%d")
            ]
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignCenter)
                self.parts_table.setItem(row, col, table_item)

    def search_parts(self):
        """البحث عن القطع"""
        search_text = self.search_input.text().strip()
        if search_text:
            parts = self.session.query(Part).filter(
                (Part.name.ilike(f'%{search_text}%')) |
                (Part.part_number.ilike(f'%{search_text}%'))
            ).all()
        else:
            parts = self.session.query(Part).all()
        self.update_table(parts)

    def add_part(self):
        """إضافة قطعة جديدة"""
        dialog = AddPartDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # التحقق من عدم وجود رقم القطعة مسبقاً
                existing_part = self.session.query(Part).filter_by(
                    part_number=dialog.part_number.text()
                ).first()
                
                if existing_part:
                    self.show_message("خأ", "رقم القطعة موجود مسبقاً", QMessageBox.Warning)
                    return

                new_part = Part(
                    part_number=dialog.part_number.text(),
                    name=dialog.name.text(),
                    type=dialog.type.currentText(),
                    quantity=int(dialog.quantity.text()),
                    cost_price=float(dialog.cost_price.text()),
                    selling_price=float(dialog.selling_price.text())
                )
                self.session.add(new_part)
                self.session.commit()
                self.load_parts()
                self.show_message("نجاح", "تمت إضافة القطعة بنجاح", QMessageBox.Information)
            except Exception as e:
                self.session.rollback()
                self.show_message("خطأ", f"حدث خطأ أثناء إضافة القطعة: {str(e)}", QMessageBox.Critical)

    def edit_part(self, item):
        """تعديل بيانات قطعة"""
        row = item.row()
        part_number = self.parts_table.item(row, 0).text()
        part = self.session.query(Part).filter_by(part_number=part_number).first()
        
        if not part:
            return
            
        dialog = AddPartDialog(self, part)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                # تحديث بيانات القطعة
                part.name = dialog.name.text()
                part.type = dialog.type.currentText()
                part.quantity = int(dialog.quantity.text())
                part.cost_price = float(dialog.cost_price.text())
                part.selling_price = float(dialog.selling_price.text())
                
                self.session.commit()
                self.load_parts()
                self.show_message("نجاح", "تم تحديث بيانات القطعة بنجاح", QMessageBox.Information)
            except Exception as e:
                self.session.rollback()
                self.show_message("خطأ", f"حدث خطأ أثناء تحديث البيانات: {str(e)}", QMessageBox.Critical)

    def delete_part(self):
        """حذف قطعة"""
        current_row = self.parts_table.currentRow()
        if current_row < 0:
            self.show_message("تنبيه", "الرجاء اختيار قطعة للحذف", QMessageBox.Warning)
            return
            
        part_number = self.parts_table.item(current_row, 0).text()
        part = self.session.query(Part).filter_by(part_number=part_number).first()
        
        if not part:
            return

        # Check if part has any sales records
        if part.sales:
            self.show_message(
                "تعذر الحذف",
                "لا يمكن حذف هذه القطعة لأنها مرتبطة بسجلات مبيعات. "
                "قم بأرشفة القطعة بدلاً من حذفها.",
                QMessageBox.Warning
            )
            return

        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف القطعة {part_number}؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.session.delete(part)
                self.session.commit()
                self.load_parts()
                self.show_message("نجاح", "تم حذف القطعة بنجاح", QMessageBox.Information)
            except Exception as e:
                self.session.rollback()
                self.show_message(
                    "خطأ",
                    "لا يمكن حذف هذه القطعة لأنها مرتبطة بسجلات أخرى",
                    QMessageBox.Critical
                )

    def show_message(self, title, message, icon):
        """عرض رسالة للمستخدم"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()

    def closeEvent(self, event):
        """إغلاق جلسة قاعدة البيانات عند إغلاق النافذة"""
        self.session.close()
        super().closeEvent(event)
 