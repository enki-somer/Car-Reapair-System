from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import sqlite3
from datetime import datetime
import hashlib

class LoginUI(QDialog):
    def __init__(self):
        super().__init__()
        self.db_path = "database/workers.db"
        self.ensure_database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("تسجيل الدخول")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                font-size: 14px;
                min-width: 250px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton#loginBtn {
                background-color: #2ecc71;
                color: white;
                border: none;
            }
            QPushButton#loginBtn:hover {
                background-color: #27ae60;
            }
            QPushButton#registerBtn {
                background-color: #3498db;
                color: white;
                border: none;
            }
            QPushButton#registerBtn:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Title
        title = QLabel("مرحباً بك في نظام إدارة الموظفين")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("اسم المستخدم:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("أدخل اسم المستخدم")
        self.username_input.setLayoutDirection(Qt.RightToLeft)
        username_layout.addWidget(self.username_input)
        username_layout.addWidget(username_label)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("كلمة المرور:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("أدخل كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setLayoutDirection(Qt.RightToLeft)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(password_label)
        layout.addLayout(password_layout)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("تسجيل الدخول")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.login)
        
        self.register_btn = QPushButton("إنشاء حساب جديد")
        self.register_btn.setObjectName("registerBtn")
        self.register_btn.clicked.connect(self.show_register_dialog)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        layout.addLayout(button_layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute("""
                SELECT id, full_name FROM users 
                WHERE username = ? AND password = ?
            """, (username, hashed_password))
            
            user = cursor.fetchone()
            conn.close()

            if user:
                self.accept()
            else:
                QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في قاعدة البيانات: {str(e)}")

    def show_register_dialog(self):
        register_dialog = RegisterUI(self)
        if register_dialog.exec_() == QDialog.Accepted:
            self.username_input.setText(register_dialog.username_input.text())
            self.password_input.setText(register_dialog.password_input.text())

    def ensure_database(self):
        """Ensure database and tables exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create users table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
            ''')
            
            # Create index if it doesn't exist
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إعداد قاعدة البيانات: {str(e)}")

    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self, 
            "تأكيد الخروج",
            "هل أنت متأكد من الخروج من التطبيق؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()  # Close the window and exit the application
            import sys
            sys.exit()
        else:
            event.ignore()  # Don't close the window

class RegisterUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.db_path = "database/workers.db"

    def init_ui(self):
        self.setWindowTitle("إنشاء حساب جديد")
        self.setGeometry(150, 150, 400, 350)
        self.setStyleSheet(self.parent().styleSheet())

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Title
        title = QLabel("إنشاء حساب جديد")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        # Full Name
        fullname_layout = QHBoxLayout()
        fullname_label = QLabel("الاسم الكامل:")
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("أدخل اسمك الكامل")
        self.fullname_input.setLayoutDirection(Qt.RightToLeft)
        fullname_layout.addWidget(self.fullname_input)
        fullname_layout.addWidget(fullname_label)
        layout.addLayout(fullname_layout)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("اسم المستخدم:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("أدخل اسم المستخدم")
        self.username_input.setLayoutDirection(Qt.RightToLeft)
        username_layout.addWidget(self.username_input)
        username_layout.addWidget(username_label)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("كلمة المرور:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("أدخل كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setLayoutDirection(Qt.RightToLeft)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(password_label)
        layout.addLayout(password_layout)

        # Confirm Password
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("تأكيد كلمة المرور:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("أعد إدخال كلمة المرور")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setLayoutDirection(Qt.RightToLeft)
        confirm_layout.addWidget(self.confirm_input)
        confirm_layout.addWidget(confirm_label)
        layout.addLayout(confirm_layout)

        # Register Button
        self.register_btn = QPushButton("إنشاء الحساب")
        self.register_btn.setObjectName("loginBtn")
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)

    def register(self):
        fullname = self.fullname_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not all([fullname, username, password, confirm]):
            QMessageBox.warning(self, "تنبيه", "الرجاء ملء جميع الحقول")
            return

        if password != confirm:
            QMessageBox.warning(self, "تنبيه", "كلمة المرور غير متطابقة")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, "تنبيه", "اسم المستخدم موجود مسبقاً")
                return

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, password, full_name, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, hashed_password, fullname, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            conn.close()

            QMessageBox.information(self, "نجاح", "تم إنشاء الحساب بنجاح")
            self.accept()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في قاعدة البيانات: {str(e)}") 