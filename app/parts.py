from typing import List, Optional
from sqlalchemy import or_
from database.models import Part
from database.db_setup import Session
from sqlalchemy.exc import SQLAlchemyError

class PartsManager:
    def __init__(self):
        self.session = Session()

    def search_parts(self, search_term: str = "") -> List[Part]:
        """
        البحث عن القطع حسب الاسم أو الرقم
        Args:
            search_term: كلمة البحث (الاسم أو رقم القطعة)
        Returns:
            قائمة بالقطع المطابقة للبحث
        """
        try:
            query = self.session.query(Part)
            
            if search_term:
                search_filter = or_(
                    Part.name.ilike(f"%{search_term}%"),
                    Part.part_number.ilike(f"%{search_term}%")
                )
                query = query.filter(search_filter)
            
            return query.all()
        except SQLAlchemyError:
            return []

    def get_part_by_number(self, part_number: str) -> Optional[Part]:
        """
        البحث عن قطعة محددة برقمها
        Args:
            part_number: رقم القطعة
        Returns:
            القطعة المطلوبة أو None إذا لم يتم العثور عليها
        """
        try:
            return self.session.query(Part).filter_by(part_number=part_number).first()
        except SQLAlchemyError:
            return None

    def get_parts_by_type(self, part_type: str) -> List[Part]:
        """
        استرجاع القطع حسب النوع
        Args:
            part_type: نوع القطعة
        Returns:
            قائمة بالقطع من النوع المحدد
        """
        try:
            return self.session.query(Part).filter_by(type=part_type).all()
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

    def close(self):
        """إغلاق جلسة قاعدة البيانات"""
        self.session.close() 