"""
数据库管理模块
功能: SQLite数据库的创建、连接和操作
"""

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_path='data/study.db'):
        """初始化数据库连接"""
        # 确保data目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """初始化数据库表结构"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 创建学习记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                duration INTEGER NOT NULL,
                timer_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建待办事项表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 2,
                status INTEGER DEFAULT 0,
                deadline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        # 创建配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化完成")
    
    # ========== 学习记录相关 ==========
    
    def add_study_record(self, duration, timer_type='pomodoro'):
        """添加学习记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO study_records (date, duration, timer_type)
            VALUES (?, ?, ?)
        ''', (today, duration, timer_type))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id
    
    def get_today_duration(self):
        """获取今日学习总时长"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT SUM(duration) FROM study_records
            WHERE date = ?
        ''', (today,))
        
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0
    
    # ========== 待办事项相关 ==========
    
    def add_todo(self, title, description='', priority=2, deadline=None):
        """添加待办事项"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO todo_items (title, description, priority, deadline)
            VALUES (?, ?, ?, ?)
        ''', (title, description, priority, deadline))
        
        conn.commit()
        todo_id = cursor.lastrowid
        conn.close()
        return todo_id
    
    def get_all_todos(self, status=None):
        """获取所有待办事项"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status is not None:
            cursor.execute('''
                SELECT * FROM todo_items
                WHERE status = ?
                ORDER BY priority ASC, created_at DESC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT * FROM todo_items
                ORDER BY priority ASC, created_at DESC
            ''')
        
        todos = cursor.fetchall()
        conn.close()
        return todos
    
    def update_todo_status(self, todo_id, status):
        """更新待办状态"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        completed_at = datetime.now() if status == 1 else None
        cursor.execute('''
            UPDATE todo_items
            SET status = ?, completed_at = ?
            WHERE id = ?
        ''', (status, completed_at, todo_id))
        
        conn.commit()
        conn.close()
    
    def delete_todo(self, todo_id):
        """删除待办事项"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM todo_items WHERE id = ?', (todo_id,))
        
        conn.commit()
        conn.close()
