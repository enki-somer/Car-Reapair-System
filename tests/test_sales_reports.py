import unittest
from datetime import datetime, timedelta
from app.sales_reports import SalesReports
from database.models import Part, Sale
from tests.conftest import setup_test_db, cleanup_test_db

class TestSalesReports(unittest.TestCase):
    def setUp(self):
        self.session, self.engine = setup_test_db()
        self.sales_reports = SalesReports()
        self.sales_reports.session = self.session
        
        # Add test part
        self.test_part = Part(
            part_number='P001',
            name='Test Part',
            quantity=100,
            cost_price=100,
            selling_price=150,
            type='Test Type'
        )
        self.session.add(self.test_part)
        self.session.commit()
        
        # Add test sales
        test_date = datetime.now()
        self.test_sales = [
            Sale(
                part_id=self.test_part.id,
                quantity=10,
                selling_price=150,
                sale_date=test_date,
                profit=500
            ),
            Sale(
                part_id=self.test_part.id,
                quantity=5,
                selling_price=150,
                sale_date=test_date - timedelta(days=1),
                profit=250
            )
        ]
        for sale in self.test_sales:
            self.session.add(sale)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()
        cleanup_test_db()

    def test_get_daily_report(self):
        report = self.sales_reports.get_daily_report(datetime.now())
        
        self.assertIsNotNone(report)
        self.assertIn('sales', report)
        self.assertIn('statistics', report)
        
        stats = report['statistics']
        self.assertEqual(stats['total_sales'], 1500)  # 10 items * 150
        self.assertEqual(stats['total_profit'], 500)
        self.assertEqual(stats['items_sold'], 10)
        self.assertEqual(stats['unique_parts'], 1)

    def test_get_monthly_report(self):
        today = datetime.now()
        report = self.sales_reports.get_monthly_report(today.year, today.month)
        
        self.assertIsNotNone(report)
        self.assertIn('sales', report)
        self.assertIn('statistics', report)
        self.assertIn('daily_stats', report)
        
        stats = report['statistics']
        self.assertEqual(stats['total_sales'], 2250)  # (10+5) items * 150
        self.assertEqual(stats['total_profit'], 750)
        self.assertEqual(stats['items_sold'], 15)

    def test_get_best_selling_parts(self):
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        best_sellers = self.sales_reports.get_best_selling_parts(
            start_date, end_date, limit=5
        )
        
        self.assertIsNotNone(best_sellers)
        self.assertEqual(len(best_sellers), 1)  # Only one part in test data
        self.assertEqual(best_sellers[0][1], 15)  # Total quantity sold

    def test_get_profit_analysis(self):
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        analysis = self.sales_reports.get_profit_analysis(start_date, end_date)
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis['total_revenue'], 2250)
        self.assertEqual(analysis['total_profit'], 750)
        self.assertGreater(analysis['profit_margin'], 0)

    def test_empty_period_report(self):
        # Test report for future date
        future_date = datetime.now() + timedelta(days=30)
        report = self.sales_reports.get_daily_report(future_date)
        
        self.assertEqual(report['statistics']['total_sales'], 0)
        self.assertEqual(report['statistics']['total_profit'], 0)
        self.assertEqual(len(report['sales']), 0)

if __name__ == '__main__':
    unittest.main() 