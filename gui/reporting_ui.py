from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem, 
                           QMessageBox, QFrame, QHeaderView, QComboBox,
                           QDateEdit, QFileDialog)
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QFont, QIcon
from database.models import Sale, Part
from database.db_setup import Session
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import func
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import xlsxwriter

class ReportingUI(QWidget):
    def __init__(self):
        super().__init__()
        self.session = Session()
        
        # Add the new styling here
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: Arial;
            }
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
            QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                min-width: 200px;
            }
            QComboBox:focus, QDateEdit:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#exportButton {
                background-color: #27ae60;
            }
            QPushButton#exportButton:hover {
                background-color: #219a52;
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
            }
            QFrame#controlFrame, QFrame#statsFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                border: 1px solid #dcdde1;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #ffffff, stop:1 #f5f6fa);
            }
            QLabel#summaryLabel {
                color: #2c3e50;
                font-size: 16px;
            }
            QLabel#valueLabel {
                color: #3498db;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        self.init_ui()
        
        # Connect to sales window if it exists
        main_window = self.parent()
        if main_window and hasattr(main_window, 'sales_window'):
            sales_ui = main_window.sales_window
            if sales_ui:
                sales_ui.sale_completed.connect(self.refresh_report)

    def init_ui(self):
        self.setWindowTitle("التقارير")
        self.setGeometry(100, 100, 1200, 800)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Control Panel
        control_frame = QFrame()
        control_frame.setObjectName("controlFrame")
        control_layout = QHBoxLayout(control_frame)

        # Report Type Selection
        report_type_label = QLabel("نوع التقرير:")
        self.report_type = QComboBox()
        self.report_type.addItems(["تقرير يومي", "تقرير شهري"])
        self.report_type.currentIndexChanged.connect(self.on_report_type_changed)

        # Date Selection
        date_label = QLabel("التاريخ:")
        self.date_select = QDateEdit()
        self.date_select.setDate(QDate.currentDate())
        self.date_select.setCalendarPopup(True)
        self.date_select.dateChanged.connect(self.generate_report)

        # Export Buttons
        self.export_csv_btn = QPushButton("تصدير CSV")
        self.export_csv_btn.setObjectName("exportButton")
        self.export_csv_btn.setIcon(QIcon("icons/csv.png"))
        self.export_csv_btn.clicked.connect(self.export_to_csv)

        self.export_pdf_btn = QPushButton("تصدير Excel")
        self.export_pdf_btn.setObjectName("pdfButton")
        self.export_pdf_btn.setIcon(QIcon("icons/excel.png"))
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)

        # Add controls to layout
        control_layout.addWidget(report_type_label)
        control_layout.addWidget(self.report_type)
        control_layout.addWidget(date_label)
        control_layout.addWidget(self.date_select)
        control_layout.addStretch()
        control_layout.addWidget(self.export_csv_btn)
        control_layout.addWidget(self.export_pdf_btn)

        # Summary Section
        summary_frame = QFrame()
        summary_frame.setObjectName("statsFrame")
        summary_layout = QHBoxLayout(summary_frame)

        # Total Items Sold
        items_sold = QVBoxLayout()
        items_sold_label = QLabel("القطع المباعة")
        items_sold_label.setObjectName("statsLabel")
        self.items_sold_value = QLabel("0")
        self.items_sold_value.setObjectName("valueLabel")
        items_sold.addWidget(items_sold_label)
        items_sold.addWidget(self.items_sold_value)

        # Total Sales
        total_sales = QVBoxLayout()
        total_sales_label = QLabel("إجمالي المبيعات")
        total_sales_label.setObjectName("statsLabel")
        self.total_sales_value = QLabel("0")
        self.total_sales_value.setObjectName("valueLabel")
        total_sales.addWidget(total_sales_label)
        total_sales.addWidget(self.total_sales_value)

        # Total Profit
        total_profit = QVBoxLayout()
        total_profit_label = QLabel("إجمالي الأرباح")
        total_profit_label.setObjectName("statsLabel")
        self.total_profit_value = QLabel("0")
        self.total_profit_value.setObjectName("valueLabel")
        total_profit.addWidget(total_profit_label)
        total_profit.addWidget(self.total_profit_value)

        # Add summary sections
        summary_layout.addLayout(items_sold)
        summary_layout.addLayout(total_sales)
        summary_layout.addLayout(total_profit)

        # Report Table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(7)
        headers = ["رقم القطعة", "اسم القطعة", "النوع", "الكمية", "سعر البيع", "الربح", "التاريخ"]
        self.report_table.setHorizontalHeaderLabels(headers)
        self.report_table.setLayoutDirection(Qt.RightToLeft)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.setAlternatingRowColors(True)

        # Add everything to main layout
        main_layout.addWidget(control_frame)
        main_layout.addWidget(summary_frame)
        main_layout.addWidget(self.report_table)
        
        self.setLayout(main_layout)
        
        # Generate initial report
        self.generate_report()

    def on_report_type_changed(self):
        """Handle report type change"""
        self.generate_report()

    def generate_report(self):
        """Generate the report based on selected type and date"""
        try:
            selected_date = self.date_select.date().toPyDate()
            
            if self.report_type.currentText() == "تقرير يومي":
                sales = self.get_daily_sales(selected_date)
            else:
                sales = self.get_monthly_sales(selected_date)
                
            self.update_table(sales)
            self.update_summary(sales)
            
        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ أثناء إنشاء التقرير: {str(e)}", QMessageBox.Critical)

    def get_daily_sales(self, date):
        """Get sales for specific day"""
        return self.session.query(
            Sale, Part
        ).join(Part).filter(
            func.date(Sale.sale_date) == date
        ).all()

    def get_monthly_sales(self, date):
        """Get sales for specific month"""
        start_date = date.replace(day=1)
        if date.month == 12:
            end_date = date.replace(year=date.year + 1, month=1, day=1)
        else:
            end_date = date.replace(month=date.month + 1, day=1)
        
        return self.session.query(
            Sale, Part
        ).join(Part).filter(
            Sale.sale_date >= start_date,
            Sale.sale_date < end_date
        ).all()

    def update_table(self, sales):
        """Update the report table with sales data"""
        self.report_table.setRowCount(len(sales))
        
        for row, (sale, part) in enumerate(sales):
            items = [
                part.part_number,
                part.name,
                part.type,
                str(sale.quantity),
                f"{sale.selling_price:,.2f}",
                f"{sale.profit:,.2f}",
                sale.sale_date.strftime("%Y-%m-%d %H:%M")
            ]
            
            for col, item in enumerate(items):
                table_item = QTableWidgetItem(str(item))
                # Align numbers to the right, text to the center
                if col in [3, 4, 5]:  # Quantity, Price, Profit columns
                    table_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    table_item.setTextAlignment(Qt.AlignCenter)
                self.report_table.setItem(row, col, table_item)

    def update_summary(self, sales):
        """Update summary statistics"""
        total_sales = sum(sale.selling_price * sale.quantity for sale, _ in sales)
        total_profit = sum(sale.profit for sale, _ in sales)
        total_items = sum(sale.quantity for sale, _ in sales)
        
        # Format numbers with right alignment
        self.total_sales_value.setText(f"{total_sales:,.2f}")
        self.total_sales_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.total_profit_value.setText(f"{total_profit:,.2f}")
        self.total_profit_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.items_sold_value.setText(f"{total_items:,}")
        self.items_sold_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def export_to_csv(self):
        """Export report to CSV file"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "حفظ التقرير", "", "CSV Files (*.csv)"
            )
            
            if filename:
                data = []
                for row in range(self.report_table.rowCount()):
                    row_data = []
                    for col in range(self.report_table.columnCount()):
                        item = self.report_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    data.append(row_data)
                
                df = pd.DataFrame(
                    data, 
                    columns=["رقم القطعة", "اسم القطعة", "النوع", "الكمية", 
                            "سعر البيع", "الربح", "التاريخ"]
                )
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                self.show_message("نجاح", "تم تصدير التقرير بنجح", QMessageBox.Information)
                
        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ أثناء تصدير التقرير: {str(e)}", QMessageBox.Critical)

    def export_to_pdf(self):
        """Export report to Excel file"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "حفظ التقرير", "", "Excel Files (*.xlsx)")
            
            if filename:
                # Create workbook and worksheet
                workbook = xlsxwriter.Workbook(filename)
                worksheet = workbook.add_worksheet()

                # Add formats
                title_format = workbook.add_format({
                    'bold': True,
                    'font_size': 16,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#34495e',
                    'font_color': 'white',
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                
                cell_format = workbook.add_format({
                    'align': 'center',
                    'valign': 'vcenter',
                    'border': 1
                })
                
                number_format = workbook.add_format({
                    'align': 'center',
                    'valign': 'vcenter',
                    'border': 1,
                    'num_format': '#,##0.00'
                })

                # Set column widths
                worksheet.set_column('A:G', 15)

                # Write title
                worksheet.merge_range('A1:G1', self.report_type.currentText(), title_format)
                worksheet.merge_range('A2:G2', self.date_select.date().toString("yyyy-MM-dd"), title_format)

                # Write summary
                worksheet.merge_range('A4:C4', f"إجمالي المبيعات: {self.total_sales_value.text()}", cell_format)
                worksheet.merge_range('D4:G4', f"إجمالي الأرباح: {self.total_profit_value.text()}", cell_format)

                # Write headers - row 6
                headers = ["رقم القطعة", "اسم القطعة", "النوع", "الكمية", "سعر البيع", "الربح", "التاريخ"]
                for col, header in enumerate(headers):
                    worksheet.write(5, col, header, header_format)

                # Write data
                for row in range(self.report_table.rowCount()):
                    for col in range(self.report_table.columnCount()):
                        item = self.report_table.item(row, col)
                        value = item.text() if item else ''
                        
                        # Use number format for numeric columns
                        if col in [3, 4, 5]:  # Quantity, Price, Profit columns
                            try:
                                value = float(value)
                                worksheet.write(row + 6, col, value, number_format)
                            except ValueError:
                                worksheet.write(row + 6, col, value, cell_format)
                        else:
                            worksheet.write(row + 6, col, value, cell_format)

                # Set RTL direction
                worksheet.right_to_left()

                # Add auto-filter
                worksheet.autofilter(5, 0, 5 + self.report_table.rowCount(), 
                                   self.report_table.columnCount() - 1)

                # Close workbook
                workbook.close()
                
                self.show_message("نجاح", "تم تصدير التقرير بنجاح", QMessageBox.Information)

        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ أثناء تصدير التقرير: {str(e)}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        """Show message dialog"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()

    def closeEvent(self, event):
        """Clean up database session on close"""
        self.session.close()
        super().closeEvent(event)

    def refresh_report(self):
        """تحديث التقرير عند إضافة مبيعات جديدة"""
        self.generate_report() 