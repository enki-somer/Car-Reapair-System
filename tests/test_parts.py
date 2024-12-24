import unittest
from unittest.mock import MagicMock
from database.models import Part
from app.parts import PartsManager


class TestPartsManager(unittest.TestCase):
    def setUp(self):
        """Set up the test environment and mock the session."""
        self.parts_manager = PartsManager()
        self.parts_manager.session = MagicMock()

    def test_search_parts_with_term(self):
        """Test searching parts with a valid search term."""
        part_mock = MagicMock()
        self.parts_manager.session.query.return_value.filter.return_value.all.return_value = [part_mock]

        result = self.parts_manager.search_parts("Brake")
        self.assertEqual(len(result), 1)
        self.parts_manager.session.query.assert_called_once()

    def test_search_parts_no_term(self):
        """Test searching parts without a search term."""
        part_mock = MagicMock()
        self.parts_manager.session.query.return_value.all.return_value = [part_mock]

        result = self.parts_manager.search_parts()
        self.assertEqual(len(result), 1)
        self.parts_manager.session.query.assert_called_once()

    def test_get_part_by_number_found(self):
        """Test retrieving a part by part number when it exists."""
        part_mock = MagicMock()
        self.parts_manager.session.query.return_value.filter_by.return_value.first.return_value = part_mock

        result = self.parts_manager.get_part_by_number("12345")
        self.assertIsNotNone(result)
        self.parts_manager.session.query.assert_called_once()

    def test_get_part_by_number_not_found(self):
        """Test retrieving a part by part number when it does not exist."""
        self.parts_manager.session.query.return_value.filter_by.return_value.first.return_value = None

        result = self.parts_manager.get_part_by_number("12345")
        self.assertIsNone(result)
        self.parts_manager.session.query.assert_called_once()

    def test_get_parts_by_type_found(self):
        """Test retrieving parts by type when they exist."""
        part_mock = MagicMock()
        self.parts_manager.session.query.return_value.filter_by.return_value.all.return_value = [part_mock]

        result = self.parts_manager.get_parts_by_type("Brakes")
        self.assertEqual(len(result), 1)
        self.parts_manager.session.query.assert_called_once()

    def test_get_parts_by_type_not_found(self):
        """Test retrieving parts by type when none exist."""
        self.parts_manager.session.query.return_value.filter_by.return_value.all.return_value = []

        result = self.parts_manager.get_parts_by_type("Brakes")
        self.assertEqual(len(result), 0)
        self.parts_manager.session.query.assert_called_once()

    def test_get_low_stock_parts_found(self):
        """Test retrieving low-stock parts when they exist."""
        part_mock = MagicMock()
        self.parts_manager.session.query.return_value.filter.return_value.all.return_value = [part_mock]

        result = self.parts_manager.get_low_stock_parts(threshold=5)
        self.assertEqual(len(result), 1)
        self.parts_manager.session.query.assert_called_once()

    def test_get_low_stock_parts_not_found(self):
        """Test retrieving low-stock parts when none exist."""
        self.parts_manager.session.query.return_value.filter.return_value.all.return_value = []

        result = self.parts_manager.get_low_stock_parts(threshold=5)
        self.assertEqual(len(result), 0)
        self.parts_manager.session.query.assert_called_once()

    def tearDown(self):
        """Clean up after tests."""
        self.parts_manager.close()


if __name__ == "__main__":
    unittest.main()
