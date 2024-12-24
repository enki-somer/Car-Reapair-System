from typing import List, Optional, Tuple, Dict
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.models import Part
from database.db_setup import Session

class InventoryManager:
    def __init__(self):
        self.session = Session()

    def validate_part_data(self, part_data: Dict) -> Tuple[bool, str]:
        """
        التحقق من صحة بيانات القطعة
        Args:
            part_data: بيانات القطعة المراد التحقق منها
        Returns:
            (صحة البيانات, رسالة الخطأ)
        """
        try:
            if not part_data.get('part_number'):
                return False, "رقم القطعة مطلوب"
            
            if not part_data.get('name'):
                return False, "اسم القطعة مطلوب"
            
            quantity = int(part_data.get('quantity', 0))
            if quantity < 0:
                return False, "الكمية يجب أن تكون أكبر من أو تساوي صفر"
            
            cost_price = float(part_data.get('cost_price', 0))
            if cost_price <= 0:
                return False, "سعر التكلفة يجب أن يكون أكبر من صفر"
            
            selling_price = float(part_data.get('selling_price', 0))
            if selling_price <= 0:
                return False, "سعر البيع يجب أن يكون أكبر من صفر"
            
            if selling_price < cost_price:
                return False, "سعر البيع يجب أن يكون أكبر من سعر التكلفة"
            
            return True, ""
            
        except ValueError:
            return False, "خطأ في تنسيق البيانات"

    def add_part(self, part_data: Dict) -> Tuple[bool, str]:
        """
        إضافة قطعة جديدة للمخزون
        Args:
            part_data: بيانات القطعة الجديدة
        Returns:
            (نجاح العملية, رسالة النتيجة)
        """
        try:
            # التحقق من صحة البيانات
            is_valid, message = self.validate_part_data(part_data)
            if not is_valid:
                return False, message

            # التحقق من عدم تكرار رقم القطعة
            existing_part = self.session.query(Part).filter_by(
                part_number=part_data['part_number']
            ).first()
            
            if existing_part:
                return False, "رقم القطعة موجود مسبقاً"

            # إنشاء قطعة جديدة
            new_part = Part(
                part_number=part_data['part_number'],
                name=part_data['name'],
                type=part_data['type'],
                quantity=int(part_data['quantity']),
                cost_price=float(part_data['cost_price']),
                selling_price=float(part_data['selling_price'])
            )

            self.session.add(new_part)
            self.session.commit()
            return True, "تمت إضافة القطعة بنجاح"

        except SQLAlchemyError as e:
            self.session.rollback()
            return False, f"خطأ في قاعدة البيانات: {str(e)}"

    def update_part(self, part_number: str, part_data: Dict) -> Tuple[bool, str]:
        """
        تحديث بيانات قطعة موجودة
        Args:
            part_number: رقم القطعة المراد تحديثها
            part_data: البيانات الجديدة
        Returns:
            (نجاح العملية, رسالة النتيجة)
        """
        try:
            # التحقق من صحة البيانات
            is_valid, message = self.validate_part_data(part_data)
            if not is_valid:
                return False, message

            part = self.session.query(Part).filter_by(part_number=part_number).first()
            if not part:
                return False, "القطعة غير موجودة"

            # تحديث البيانات
            part.name = part_data['name']
            part.type = part_data['type']
            part.quantity = int(part_data['quantity'])
            part.cost_price = float(part_data['cost_price'])
            part.selling_price = float(part_data['selling_price'])

            self.session.commit()
            return True, "تم تحديث بيانات القطعة بنجاح"

        except SQLAlchemyError as e:
            self.session.rollback()
            return False, f"خطأ في قاعدة البيانات: {str(e)}"

    def delete_part(self, part_number: str) -> Tuple[bool, str]:
        """
        حذف قطعة من المخزون
        Args:
            part_number: رقم القطعة المراد حذفها
        Returns:
            (نجاح العملية, رسالة النتيجة)
        """
        try:
            part = self.session.query(Part).filter_by(part_number=part_number).first()
            if not part:
                return False, "القطعة غير موجودة"

            self.session.delete(part)
            self.session.commit()
            return True, "تم حذف القطعة بنجاح"

        except SQLAlchemyError as e:
            self.session.rollback()
            return False, f"خطأ في قاعدة البيانات: {str(e)}"

    def search_parts(self, search_term: str = "") -> List[Part]:
        """
        البحث عن القطع
        Args:
            search_term: كلمة البحث (الاسم أو رقم القطعة)
        Returns:
            قائمة بالقطع المطابقة
        """
        try:
            query = self.session.query(Part)
            if search_term:
                query = query.filter(
                    (Part.name.ilike(f'%{search_term}%')) |
                    (Part.part_number.ilike(f'%{search_term}%'))
                )
            return query.all()
        except SQLAlchemyError:
            return []

    def get_low_stock_parts(self, threshold: int = 5) -> List[Part]:
        """
        استرجاع القطع التي وصلت لحد إعادة الطلب
        Args:
            threshold: حد إعادة الطلب
        Returns:
            قائمة بالقطع التي تحتاج إعادة طلب
        """
        try:
            return self.session.query(Part).filter(Part.quantity <= threshold).all()
        except SQLAlchemyError:
            return []

    def get_part_by_number(self, part_number: str) -> Optional[Part]:
        """
        استرجاع قطعة محددة برقمها
        Args:
            part_number: رقم القطعة
        Returns:
            القطعة المطلوبة أو None
        """
        try:
            return self.session.query(Part).filter_by(part_number=part_number).first()
        except SQLAlchemyError:
            return None

    def close(self):
        """إغلاق جلسة قاعدة البيانات"""
        self.session.close() 