import unittest
from unittest.mock import patch, MagicMock
from app.reports import AttendanceReports
import sqlite3


class TestAttendanceReports(unittest.TestCase):
    def setUp(self):
        """Set up the test class with an instance of AttendanceReports."""
        self.reports = AttendanceReports(db_path=":memory:")

    @patch("app.reports.sqlite3.connect")
    def test_generate_daily_report(self, mock_connect):
        """Test daily report generation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.row_factory = sqlite3.Row

        # Mocking the database return
        mock_cursor.fetchall.return_value = [
            {
                "name": "John Doe",
                "phone": "123456789",
                "date": "2024-11-01",
                "time_in": "09:00:00",
                "time_out": "17:00:00",
                "status": "حاضر",
                "salary": 3000
            }
        ]

        result = self.reports.generate_daily_report("2024-11-01")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John Doe")
        mock_connect.assert_called_once_with(":memory:")

    @patch("app.reports.sqlite3.connect")
    def test_generate_monthly_report(self, mock_connect):
        """Test monthly report generation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.row_factory = sqlite3.Row

        # Mocking the database return
        mock_cursor.fetchall.return_value = [
            {
                "id": 1,
                "name": "Jane Doe",
                "salary": 3000,
                "present_days": 20,
                "absent_days": 5,
                "late_days": 3,
                "vacation_days": 2,
            }
        ]

        result = self.reports.generate_monthly_report(2024, 11)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Jane Doe")
        self.assertEqual(result[0]["absent_days"], 5)
        mock_connect.assert_called_once_with(":memory:")

    @patch("app.reports.sqlite3.connect")
    def test_calculate_salary(self, mock_connect):
        """Test salary calculation."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.row_factory = sqlite3.Row

        # Mocking worker salary
        mock_cursor.fetchone.side_effect = [
            {"salary": 3000},  # Worker salary
            {"absent_days": 5, "late_days": 3}  # Attendance stats
        ]

        result = self.reports.calculate_salary(worker_id=1, year=2024, month=11)
        self.assertIsNotNone(result)
        self.assertEqual(result["base_salary"], 3000)
        self.assertEqual(result["absent_days"], 5)
        self.assertEqual(result["late_days"], 3)
        self.assertAlmostEqual(result["final_salary"], 2425.0)  # Updated expected value

        mock_connect.assert_called_once_with(":memory:")

    def tearDown(self):
        """Clean up resources."""
        self.reports = None


if __name__ == "__main__":
    unittest.main()
