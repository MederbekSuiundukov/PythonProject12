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
        conn.close()

    def add_task(self, task_data):
        """Добавляем новую задачу в базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        conn.close()
