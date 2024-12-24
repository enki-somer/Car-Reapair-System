import sqlite3
from contextlib import closing

DATABASE = 'company.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def add_worker(name, phone, salary):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Workers (name, phone, salary) VALUES (?, ?, ?)
        ''', (name, phone, salary))
        return cursor.lastrowid

def get_worker(worker_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Workers WHERE id = ?', (worker_id,))
        return cursor.fetchone()

def update_worker(worker_id, name=None, phone=None, salary=None):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE Workers SET name = ? WHERE id = ?', (name, worker_id))
        if phone:
            cursor.execute('UPDATE Workers SET phone = ? WHERE id = ?', (phone, worker_id))
        if salary:
            cursor.execute('UPDATE Workers SET salary = ? WHERE id = ?', (salary, worker_id))

def delete_worker(worker_id):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Workers WHERE id = ?', (worker_id,))

def list_workers():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, phone, salary FROM Workers')
        return cursor.fetchall()

def update_attendance(worker_id, date, status):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Attendance (worker_id, date, status)
            VALUES (?, ?, ?)
            ON CONFLICT(worker_id, date) DO UPDATE SET status=excluded.status
        ''', (worker_id, date, status))

def delete_all_workers():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Workers')
        conn.commit()
