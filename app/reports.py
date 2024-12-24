import sqlite3
from datetime import datetime, timedelta
import calendar
from PyQt5.QtWidgets import QMessageBox

class AttendanceReports:
    def __init__(self, db_path="database/workers.db"):
        self.db_path = db_path

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {str(e)}")
            return None

    def generate_daily_report(self, date):
        """Generate daily attendance report for specific date"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    w.name,
                    w.phone,
                    a.date,
                    a.time_in,
                    a.time_out,
                    a.status,
                    w.salary
                FROM attendance a
                JOIN workers w ON a.worker_id = w.id
                WHERE a.date = ?
                ORDER BY w.name
            """, (date,))
            
            report_data = cursor.fetchall()
            conn.close()
            
            return report_data
            
        except sqlite3.Error as e:
            print(f"Error generating daily report: {str(e)}")
            return None

    def generate_monthly_report(self, year, month):
        """Generate monthly attendance report"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            
            # Get the number of days in the month
            num_days = calendar.monthrange(year, month)[1]
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{num_days}"
            
            cursor.execute("""
                SELECT 
                    w.id,
                    w.name,
                    w.salary,
                    COUNT(CASE WHEN a.status = 'حاضر' THEN 1 END) as present_days,
                    COUNT(CASE WHEN a.status = 'غائب' THEN 1 END) as absent_days,
                    COUNT(CASE WHEN a.status = 'متأخر' THEN 1 END) as late_days,
                    COUNT(CASE WHEN a.status = 'إجازة' THEN 1 END) as vacation_days
                FROM workers w
                LEFT JOIN attendance a ON w.id = a.worker_id 
                    AND a.date BETWEEN ? AND ?
                WHERE w.status = 'نشط'
                GROUP BY w.id
                ORDER BY w.name
            """, (start_date, end_date))
            
            report_data = cursor.fetchall()
            conn.close()
            
            return report_data
            
        except sqlite3.Error as e:
            print(f"Error generating monthly report: {str(e)}")
            return None

    def calculate_salary(self, worker_id, year, month):
        """Calculate worker's salary for the month including deductions"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            
            # Get worker's base salary
            cursor.execute("SELECT salary FROM workers WHERE id = ?", (worker_id,))
            worker = cursor.fetchone()
            if not worker:
                return None
                
            base_salary = worker['salary']
            
            # Get attendance records for the month
            num_days = calendar.monthrange(year, month)[1]
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{num_days}"
            
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'غائب' THEN 1 END) as absent_days,
                    COUNT(CASE WHEN status = 'متأخر' THEN 1 END) as late_days
                FROM attendance 
                WHERE worker_id = ? AND date BETWEEN ? AND ?
            """, (worker_id, start_date, end_date))
            
            attendance = cursor.fetchone()
            conn.close()
            
            # Calculate deductions
            daily_rate = base_salary / 30  # Assuming 30 days per month
            absent_deduction = attendance['absent_days'] * daily_rate
            late_deduction = attendance['late_days'] * (daily_rate * 0.25)  # 25% deduction for late days
            
            # Calculate final salary
            final_salary = base_salary - absent_deduction - late_deduction
            
            return {
                'base_salary': base_salary,
                'absent_days': attendance['absent_days'],
                'late_days': attendance['late_days'],
                'absent_deduction': absent_deduction,
                'late_deduction': late_deduction,
                'final_salary': final_salary
            }
            
        except sqlite3.Error as e:
            print(f"Error calculating salary: {str(e)}")
            return None