import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('road_safety.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT,
            timestamp DATETIME,
            image_path TEXT
        )''')
        self.conn.commit()

    def log_violation(self, plate_number, image_path):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO violations (plate_number, timestamp, image_path)
        VALUES (?, ?, ?)
        ''', (plate_number, datetime.now(), image_path))
        self.conn.commit()
