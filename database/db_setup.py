import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite setup
def setup_database():
    # Ensure the database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('database/workers.db')
    cursor = conn.cursor()

    # Create workers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        salary INTEGER NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL
    )
    ''')

    # Create attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL,
        date DATE NOT NULL,
        time_in TIMESTAMP,
        time_out TIMESTAMP,
        status TEXT DEFAULT 'present',
        notes TEXT,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (worker_id) REFERENCES workers(id),
        UNIQUE(worker_id, date)
    )
    ''')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_worker_name ON workers(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_worker_phone ON workers(phone)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_worker ON attendance(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')

    conn.commit()
    conn.close()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///database/workers.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Create Session class
Session = sessionmaker(bind=engine)

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Set up SQLite tables first
    setup_database()
    
    # Import models and create SQLAlchemy tables
    from . import models
    Base.metadata.create_all(bind=engine)
    
    # Create a session and initialize any required data
    session = Session()
    try:
        # You can add any initial data here if needed
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")
    finally:
        session.close()

def get_db():
    """Return SQLite database connection"""
    return sqlite3.connect('database/workers.db')

def get_session():
    """Return SQLAlchemy session"""
    return Session()

if __name__ == "__main__":
    setup_database()
