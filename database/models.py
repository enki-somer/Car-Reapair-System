import sqlite3
from contextlib import closing
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db_setup import Base  # Import Base from db_setup instead of creating a new one

class Part(Base):
    """نموذج قطع الغيار"""
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    part_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    quantity = Column(Integer, default=0)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float)
    
    # العلاقة مع جدول المبيعات مع إضافة cascade
    sales = relationship("Sale", back_populates="part", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Part(name='{self.name}', part_number='{self.part_number}')>"


class Sale(Base):
    """نموذج المبيعات"""
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    selling_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.now)
    profit = Column(Float)

    # العلاقة مع جدول القطع
    part = relationship("Part", back_populates="sales")

    def __repr__(self):
        return f"<Sale(part_id={self.part_id}, quantity={self.quantity}, date='{self.sale_date}')>"

# Keep the existing SQLite functions below if needed
def connect_db():
    return sqlite3.connect('company.db')

# Workers Table Functions
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
        cursor.execute('SELECT * FROM Workers')
        return cursor.fetchall()

# Inventory Table Functions
def add_inventory_item(item_name, category, type, part_number, wholesale_price, quantity, status):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Inventory (item_name, category, type, part_number, wholesale_price, quantity, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item_name, category, type, part_number, wholesale_price, quantity, status))
        return cursor.lastrowid

def get_inventory_item(item_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Inventory WHERE id = ?', (item_id,))
        return cursor.fetchone()

def update_inventory_item(item_id, **kwargs):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE Inventory SET {key} = ? WHERE id = ?', (value, item_id))

def delete_inventory_item(item_id):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Inventory WHERE id = ?', (item_id,))

def list_inventory_items():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Inventory')
        return cursor.fetchall()

# Sales Table Functions
def add_sale(item_id, sold_price, date, profit):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Sales (item_id, sold_price, date, profit) VALUES (?, ?, ?, ?)
        ''', (item_id, sold_price, date, profit))
        return cursor.lastrowid

def get_sale(sale_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Sales WHERE id = ?', (sale_id,))
        return cursor.fetchone()

def update_sale(sale_id, **kwargs):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE Sales SET {key} = ? WHERE id = ?', (value, sale_id))

def delete_sale(sale_id):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Sales WHERE id = ?', (sale_id,))

def list_sales():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Sales')
        return cursor.fetchall()

# Attendance Table Functions
def add_attendance(worker_id, date, status):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Attendance (worker_id, date, status) VALUES (?, ?, ?)
        ''', (worker_id, date, status))
        return cursor.lastrowid

def get_attendance(attendance_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Attendance WHERE id = ?', (attendance_id,))
        return cursor.fetchone()

def update_attendance(attendance_id, **kwargs):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE Attendance SET {key} = ? WHERE id = ?', (value, attendance_id))

def delete_attendance(attendance_id):
    with closing(connect_db()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Attendance WHERE id = ?', (attendance_id,))

def list_attendance():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Attendance')
        return cursor.fetchall()
