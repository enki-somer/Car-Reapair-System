import unittest
from datetime import datetime
from app.sales import SalesManager
from database.models import Part
from tests.conftest import setup_test_db, cleanup_test_db

class TestSalesManager(unittest.TestCase):
    def setUp(self):
        self.session, self.engine = setup_test_db()
        self.sales = SalesManager()
        self.sales.session = self.session
        
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

    def tearDown(self):
        self.session.close()
        self.engine.dispose()
        cleanup_test_db()

    def test_validate_sale(self):
        # Test valid sale
        is_valid, message = self.sales.validate_sale(
            self.test_part, quantity=10, selling_price=150
        )
        self.assertTrue(is_valid)

        # Test invalid quantity
        is_valid, message = self.sales.validate_sale(
            self.test_part, quantity=0, selling_price=150
        )
        self.assertFalse(is_valid)
        self.assertEqual(message, "الكمية يجب أن تكون أكبر من صفر")

        # Test insufficient stock
        is_valid, message = self.sales.validate_sale(
            self.test_part, quantity=101, selling_price=150
        )
        self.assertFalse(is_valid)
        self.assertEqual(message, "الكمية المطلوبة غير متوفرة في المخزون")

    def test_create_sale(self):
        # Test valid sale
        success, message = self.sales.create_sale('P001', 10, 150)
        self.assertTrue(success)
        
        # Verify inventory update
        self.assertEqual(self.test_part.quantity, 90)

        # Test invalid part number
        success, message = self.sales.create_sale('INVALID', 10, 150)
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main() 