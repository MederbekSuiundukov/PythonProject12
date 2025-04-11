import sqlite3
from task_dialog import TaskDialog  # Импортируем TaskDialog
from task_dao import TaskDAO
def check_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)
    conn.close()

check_tasks()
