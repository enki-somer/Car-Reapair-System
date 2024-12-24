"""
Test Configuration Module

This module provides the test configuration and database setup for the test suite.
It includes functions for creating and cleaning up test databases.

Functions:
    setup_test_db(): Sets up SQLAlchemy test database
    setup_test_sqlite_db(): Sets up SQLite test database for workers
    cleanup_test_db(): Cleans up test databases
"""

import os
import sys
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test database configuration
TEST_DB_PATH = "test_database.db"
TEST_SQLITE_DB = "test_workers.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

def setup_test_db():
    """Setup test database"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    return Session(), engine

def setup_test_sqlite_db():
    """Setup test SQLite database for workers"""
    # First, cleanup any existing database
    cleanup_test_db()
    
    conn = sqlite3.connect(TEST_SQLITE_DB)
    cursor = conn.cursor()
    
    # Create Workers table with status column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            salary REAL,
            status TEXT DEFAULT 'نشط'
        )
    ''')
    
    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER,
            date TEXT,
            status TEXT,
            time_in TEXT,
            time_out TEXT,
            FOREIGN KEY (worker_id) REFERENCES Workers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def cleanup_test_db():
    """Cleanup test databases"""
    try:
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        if os.path.exists(TEST_SQLITE_DB):
            os.remove(TEST_SQLITE_DB)
    except PermissionError:
        print("Warning: Could not remove test database file immediately") 