import sqlite3
from werkzeug.security import generate_password_hash
import os

def get_db_connection():
    db_path = os.getenv('DATABASE', 'scss.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')

    # Create Bookings table (Classrooms & Labs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room TEXT NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            status TEXT DEFAULT 'Confirmed',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create Maintenance Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            technician_assigned TEXT DEFAULT 'None',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Insert default users if they don't exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ('admin@unikl.edu.my', generate_password_hash('password123'), 'admin', 'System Admin'),
            ('student@unikl.edu.my', generate_password_hash('password123'), 'student', 'John Doe'),
            ('student2@unikl.edu.my', generate_password_hash('password123'), 'student', 'Jane Smith'),
            ('lecturer@unikl.edu.my', generate_password_hash('password123'), 'lecturer', 'Dr. Smith')
        ]
        cursor.executemany("INSERT INTO users (email, password_hash, role, name) VALUES (?, ?, ?, ?)", default_users)
        print("Default users initialized.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    init_db()
    print("Database initialized successfully.")
