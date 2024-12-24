from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from database.models import Sale, Part
from database.db_setup import Session

class SalesReports:
    def __init__(self):
        self.session = Session()

    def get_daily_report(self, date: datetime) -> Dict:
        """
        إنشاء تقرير المبيعات اليومي
        Args:
            date: تاريخ التقرير
        Returns:
            تقرير يتضمن تفاصيل المبيعات والإحصائيات
        """
        try:
            # الحصول على جميع مبيعات اليوم
            sales = self.session.query(
                Sale, Part
            ).join(Part).filter(
                func.date(Sale.sale_date) == date.date()
            ).all()

            # حساب الإحصائيات
            total_sales = sum(sale.selling_price * sale.quantity for sale, _ in sales)
            total_profit = sum(sale.profit for sale, _ in sales)
            items_sold = sum(sale.quantity for sale, _ in sales)
            unique_parts = len(set(part.id for _, part in sales))

            return {
                'sales': sales,
                'statistics': {
                    'total_sales': total_sales,
                    'total_profit': total_profit,
                    'items_sold': items_sold,
                    'unique_parts': unique_parts
                },
                'date': date.strftime("%Y-%m-%d")
            }

        except SQLAlchemyError as e:
            print(f"خطأ في قاعدة البيانات: {str(e)}")
            return self.get_empty_report()

    def get_monthly_report(self, year: int, month: int) -> Dict:
        """
        إنشاء تقرير المبيعات الشهري
        Args:
            year: السنة
            month: الشهر
        Returns:
            تقرير يتضمن تفاصيل المبيعات والإحصائيات
        """
        try:
            # تحديد بداية ونهاية الشهر
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            # الحصول على جميع مبيعات الشهر
            sales = self.session.query(
                Sale, Part
            ).join(Part).filter(
                and_(
                    Sale.sale_date >= start_date,
                    Sale.sale_date < end_date
                )
            ).all()

            # تجميع البيانات حسب اليوم
            daily_stats = {}
            for sale, part in sales:
                day = sale.sale_date.date()
                if day not in daily_stats:
                    daily_stats[day] = {
                        'sales': 0,
                        'profit': 0,
                        'items': 0
                    }
                daily_stats[day]['sales'] += sale.selling_price * sale.quantity
                daily_stats[day]['profit'] += sale.profit
                daily_stats[day]['items'] += sale.quantity

            # حساب الإحصائيات الإجمالية
            total_sales = sum(sale.selling_price * sale.quantity for sale, _ in sales)
            total_profit = sum(sale.profit for sale, _ in sales)
            items_sold = sum(sale.quantity for sale, _ in sales)
            unique_parts = len(set(part.id for _, part in sales))

            return {
                'sales': sales,
                'daily_stats': daily_stats,
                'statistics': {
                    'total_sales': total_sales,
                    'total_profit': total_profit,
                    'items_sold': items_sold,
                    'unique_parts': unique_parts,
                    'average_daily_sales': total_sales / len(daily_stats) if daily_stats else 0
                },
                'period': f"{year}-{month:02d}"
            }

        except SQLAlchemyError as e:
            print(f"خطأ في قاعدة البيانات: {str(e)}")
            return self.get_empty_report()

    def get_best_selling_parts(self, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Tuple]:
        """
        الحصول على أكثر القطع مبيعاً
        Args:
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            limit: عدد القطع المراد عرضها
        Returns:
            قائمة بأكثر القطع مبيعاً
        """
        try:
            return self.session.query(
                Part,
                func.sum(Sale.quantity).label('total_quantity'),
                func.sum(Sale.profit).label('total_profit')
            ).join(Sale).filter(
                and_(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                )
            ).group_by(Part.id).order_by(
                func.sum(Sale.quantity).desc()
            ).limit(limit).all()
        except SQLAlchemyError:
            return []

    def get_profit_analysis(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        تحليل الأرباح خلال فترة محددة
        Args:
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
        Returns:
            تحليل تفصيلي للأرباح
        """
        try:
            sales = self.session.query(
                Sale, Part
            ).join(Part).filter(
                and_(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                )
            ).all()

            total_revenue = sum(sale.selling_price * sale.quantity for sale, _ in sales)
            total_cost = sum(part.cost_price * sale.quantity for sale, part in sales)
            total_profit = sum(sale.profit for sale, _ in sales)

            return {
                'total_revenue': total_revenue,
                'total_cost': total_cost,
                'total_profit': total_profit,
                'profit_margin': (total_profit / total_revenue * 100) if total_revenue > 0 else 0,
                'average_profit_per_sale': total_profit / len(sales) if sales else 0
            }
        except SQLAlchemyError:
            return {
                'total_revenue': 0,
                'total_cost': 0,
                'total_profit': 0,
                'profit_margin': 0,
                'average_profit_per_sale': 0
            }

    def get_empty_report(self) -> Dict:
        """إنشاء تقرير فارغ في حالة حدوث خطأ"""
        return {
            'sales': [],
            'statistics': {
                'total_sales': 0,
                'total_profit': 0,
                'items_sold': 0,
                'unique_parts': 0
            },
            'date': datetime.now().strftime("%Y-%m-%d")
        }

    def close(self):
        """إغلاق جلسة قاعدة البيانات"""
        self.session.close() 