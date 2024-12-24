import unittest
import sqlite3
from datetime import date
from app.workers import *
from tests.conftest import setup_test_sqlite_db, cleanup_test_db

class TestWorkers(unittest.TestCase):
    def setUp(self):
        setup_test_sqlite_db()
        self.test_worker_data = {
            'name': 'Test Worker',
            'phone': '1234567890',
            'salary': 5000.0
        }

    def tearDown(self):
        cleanup_test_db()
        
    def test_add_worker(self):
        worker_id = add_worker(
            self.test_worker_data['name'],
            self.test_worker_data['phone'],
            self.test_worker_data['salary']
        )
        
        self.assertIsNotNone(worker_id)
        
        # Verify worker was added
        worker = get_worker(worker_id)
        self.assertIsNotNone(worker)
        self.assertEqual(worker[1], self.test_worker_data['name'])

    def test_update_worker(self):
        # First add a worker
        worker_id = add_worker(
            self.test_worker_data['name'],
            self.test_worker_data['phone'],
            self.test_worker_data['salary']
        )
        
        # Update worker
        new_name = "Updated Worker"
        update_worker(worker_id, name=new_name)
        
        # Verify update
        worker = get_worker(worker_id)
        self.assertEqual(worker[1], new_name)

    def test_delete_worker(self):
        # First add a worker
        worker_id = add_worker(
            self.test_worker_data['name'],
            self.test_worker_data['phone'],
            self.test_worker_data['salary']
        )
        
        # Delete worker
        delete_worker(worker_id)
        
        # Verify deletion
        worker = get_worker(worker_id)
        self.assertIsNone(worker)

    def test_list_workers(self):
        # Add multiple workers
        worker_ids = []
        for i in range(3):
            worker_id = add_worker(
                f"Worker {i}",
                f"123456789{i}",
                5000.0
            )
            worker_ids.append(worker_id)
        
        # Get list of workers
        workers = list_workers()
        
        self.assertEqual(len(workers), 3)
        self.assertEqual(workers[0][1], "Worker 0")

    def test_update_attendance(self):
        # Add a worker
        worker_id = add_worker(
            self.test_worker_data['name'],
            self.test_worker_data['phone'],
            self.test_worker_data['salary']
        )
        
        # Update attendance
        today = date.today().strftime("%Y-%m-%d")
        update_attendance(worker_id, today, "حاضر")
        
        # Verify attendance
        conn = sqlite3.connect("test_workers.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM attendance WHERE worker_id = ? AND date = ?",
            (worker_id, today)
        )
        attendance = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(attendance)
        self.assertEqual(attendance[0], "حاضر")

    def test_delete_all_workers(self):
        # Add multiple workers
        for i in range(3):
            add_worker(
                f"Worker {i}",
                f"123456789{i}",
                5000.0
            )
        
        # Delete all workers
        delete_all_workers()
        
        # Verify all workers were deleted
        workers = list_workers()
        self.assertEqual(len(workers), 0)

if __name__ == '__main__':
    unittest.main() 