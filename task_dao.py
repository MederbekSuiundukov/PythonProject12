import sqlite3

class TaskDAO:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Создаём таблицу tasks, если она ещё не существует"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority TEXT,
                deadline TEXT,
                status TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()


    def add_task(self, task_data):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, category, priority, deadline, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data['title'],
                task_data['description'],
                task_data['category'],
                task_data['priority'],
                task_data['deadline'],
                task_data['status'],
                task_data['created_at']
            ))
            conn.commit()


