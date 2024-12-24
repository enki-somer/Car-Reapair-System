from datetime import datetime
from database.models import Part, Sale
from database.db_setup import Session
from sqlalchemy.exc import SQLAlchemyError

class SalesManager:
    def __init__(self):
        self.session = Session()

    def validate_sale(self, part: Part, quantity: int, selling_price: float):
        """التحقق من صحة عملية البيع"""
        if not part:
            return False, "لم يتم العثور على القطعة"
        
        if quantity <= 0:
            return False, "الكمية يجب أن تكون أكبر من صفر"
            
        if quantity > part.quantity:
            return False, "الكمية المطلوبة غير متوفرة في المخزون"
        
        if selling_price <= 0:
            return False, "سعر البيع يجب أن يكون أكبر من صفر"
            
        return True, ""

    def create_sale(self, part_number: str, quantity: int, selling_price: float):
        """تسجيل عملية بيع جديدة"""
        try:
            # البحث عن القطعة
            part = self.session.query(Part).filter_by(part_number=part_number).first()
            
            # التحقق من صحة البيانات
            is_valid, message = self.validate_sale(part, quantity, selling_price)
            if not is_valid:
                return False, message

            # حساب الربح
            profit = (selling_price - part.cost_price) * quantity

            # إنشاء سجل البيع
            new_sale = Sale(
                part_id=part.id,
                quantity=quantity,
                selling_price=selling_price,
                sale_date=datetime.now(),
                profit=profit
            )

            # تحديث المخزون
            part.quantity -= quantity

            # حفظ التغييرات
            self.session.add(new_sale)
            self.session.commit()
            
            return True, "تم تسجيل عملية البيع بنجاح"

        except SQLAlchemyError as e:
            self.session.rollback()
            return False, f"خطأ في قاعدة البيانات: {str(e)}"

    def get_sales_report(self, start_date: datetime, end_date: datetime):
        """استخراج تقرير المبيعات"""
        try:
            sales = self.session.query(Sale).filter(
                Sale.sale_date.between(start_date, end_date)
            ).all()
            
            total_sales = len(sales)
            total_profit = sum(sale.profit for sale in sales)
            
            return {
                'sales': sales,
                'total_sales': total_sales,
                'total_profit': total_profit
            }
            
        except SQLAlchemyError:
            return {
                'sales': [],
                'total_sales': 0,
                'total_profit': 0
            }

    def close(self):
        """إغلاق جلسة قاعدة البيانات"""
        self.session.close() 