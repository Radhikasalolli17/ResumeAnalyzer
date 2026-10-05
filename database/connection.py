import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "cv")
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
             self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password)
             self.cursor = self.conn.cursor()
             self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
             self.conn.select_db(self.database)
             self.create_tables()
             return True
        except Exception as e:
             print(f"Database connection error: {e}")
             return False

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), phone VARCHAR(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS resume_analysis (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, target_role VARCHAR(255), ats_score FLOAT, job_match_score FLOAT, filename VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS feedback (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), rating INT, comments TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.conn.commit()

    def insert_user(self, name, email, phone):
        self.cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def insert_analysis(self, user_id, target_role, ats_score, job_match_score, filename):
        self.cursor.execute("INSERT INTO resume_analysis (user_id, target_role, ats_score, job_match_score, filename) VALUES (%s, %s, %s, %s, %s)", (user_id, target_role, ats_score, job_match_score, filename))
        self.conn.commit()

    def insert_feedback(self, name, email, rating, comments):
        self.cursor.execute("INSERT INTO feedback (name, email, rating, comments) VALUES (%s, %s, %s, %s)", (name, email, rating, comments))
        self.conn.commit()

    def get_admin_stats(self):
        stats = {}
        self.cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT AVG(ats_score) FROM resume_analysis")
        avg = self.cursor.fetchone()[0]
        stats['avg_ats_score'] = round(avg, 2) if avg else 0
        self.cursor.execute("SELECT target_role, COUNT(*) as c FROM resume_analysis GROUP BY target_role ORDER BY c DESC LIMIT 5")
        stats['top_roles'] = self.cursor.fetchall()
        return stats
        
    def close(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()
