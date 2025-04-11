import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from task_dialog import TaskDialog  # импортируем твой диалог

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskMaster")

        # Кнопка "Добавить задачу"
        self.button = QPushButton("Добавить задачу")
        self.button.clicked.connect(self.open_task_dialog)

        # Оформление
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_task_dialog(self):
        dialog = TaskDialog()
        if dialog.exec():  # Если нажали "Сохранить"
            data = dialog.get_data()
            self.save_to_db(data)

    def save_to_db(self, data):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, category, priority, deadline, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            data['title'],
            data['description'],
            data['category'],
            data['priority'],
            data['deadline'],
            data['status']
        ))

        conn.commit()
        conn.close()
        print("Задача сохранена!")

# Запуск
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())


