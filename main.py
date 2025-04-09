import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from task_dialog import TaskDialog  # Импортируем TaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskMaster")
        self.setGeometry(100, 100, 600, 400)

        # Кнопка для открытия окна добавления/редактирования задачи
        self.openDialogButton = QPushButton("Добавить задачу", self)
        self.openDialogButton.clicked.connect(self.open_task_dialog)
        self.openDialogButton.setGeometry(100, 100, 200, 50)

    def open_task_dialog(self):
        dialog = TaskDialog()  # Создаём объект диалогового окна
        if dialog.exec():  # Если окно было закрыто с помощью кнопки "Сохранить"
            task_data = dialog.get_data()  # Получаем введённые данные
            print(task_data)  # Выводим данные (или сохраняем их в БД)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import sqlite3

