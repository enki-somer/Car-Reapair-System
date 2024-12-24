import unittest
from unittest.mock import MagicMock, patch
from database.models import Part
from app.inventory import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Set up the test environment and mock the session."""
        self.inventory_manager = InventoryManager()
        self.inventory_manager.session = MagicMock()

    def test_validate_part_data_valid(self):
        """Test part data validation with valid data."""
        part_data = {
            "part_number": "12345",
            "name": "Brake Pad",
            "quantity": 10,
            "cost_price": 50.0,
            "selling_price": 70.0,
        }
        result, message = self.inventory_manager.validate_part_data(part_data)
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_validate_part_data_invalid(self):
        """Test part data validation with invalid data."""
        part_data = {
            "part_number": "12345",
            "name": "",
            "quantity": -5,
            "cost_price": 50.0,
            "selling_price": 40.0,
        }
        result, message = self.inventory_manager.validate_part_data(part_data)
        self.assertFalse(result)
        self.assertEqual(message, "اسم القطعة مطلوب")  # Adjust based on error checks order

    def test_add_part_success(self):
        """Test adding a new part successfully."""
        part_data = {
            "part_number": "12345",
            "name": "Brake Pad",
            "type": "Brakes",
            "quantity": 10,
            "cost_price": 50.0,
            "selling_price": 70.0,
        }

        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = None
        self.inventory_manager.session.add.return_value = None

        result, message = self.inventory_manager.add_part(part_data)
        self.assertTrue(result)
        self.assertEqual(message, "تمت إضافة القطعة بنجاح")

    def test_add_part_duplicate(self):
        """Test adding a part that already exists."""
        part_data = {
            "part_number": "12345",
            "name": "Brake Pad",
            "type": "Brakes",
            "quantity": 10,
            "cost_price": 50.0,
            "selling_price": 70.0,
        }

        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = Part()

        result, message = self.inventory_manager.add_part(part_data)
        self.assertFalse(result)
        self.assertEqual(message, "رقم القطعة موجود مسبقاً")

    def test_delete_part_success(self):
        """Test deleting a part successfully."""
        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = Part()

        result, message = self.inventory_manager.delete_part("12345")
        self.assertTrue(result)
        self.assertEqual(message, "تم حذف القطعة بنجاح")

    def test_delete_part_not_found(self):
        """Test deleting a part that doesn't exist."""
        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = None

        result, message = self.inventory_manager.delete_part("12345")
        self.assertFalse(result)
        self.assertEqual(message, "القطعة غير موجودة")

    def test_search_parts(self):
        """Test searching for parts."""
        part_mock = MagicMock()
        self.inventory_manager.session.query.return_value.filter.return_value.all.return_value = [part_mock]

        result = self.inventory_manager.search_parts("Brake")
        self.assertEqual(len(result), 1)

    def test_get_low_stock_parts(self):
        """Test retrieving parts below stock threshold."""
        part_mock = MagicMock()
        self.inventory_manager.session.query.return_value.filter.return_value.all.return_value = [part_mock]

        result = self.inventory_manager.get_low_stock_parts(threshold=5)
        self.assertEqual(len(result), 1)

    def test_get_part_by_number_found(self):
        """Test retrieving a part by number when found."""
        part_mock = MagicMock()
        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = part_mock

        result = self.inventory_manager.get_part_by_number("12345")
        self.assertIsNotNone(result)

    def test_get_part_by_number_not_found(self):
        """Test retrieving a part by number when not found."""
        self.inventory_manager.session.query.return_value.filter_by.return_value.first.return_value = None

        result = self.inventory_manager.get_part_by_number("12345")
        self.assertIsNone(result)

    def tearDown(self):
        """Clean up after tests."""
        self.inventory_manager.close()


if __name__ == "__main__":
    unittest.main()
