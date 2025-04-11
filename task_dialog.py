from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableView, QDialog, QVBoxLayout, QLineEdit, QTextEdit, QComboBox, QDateEdit, \
    QDialogButtonBox, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QDate, QAbstractTableModel, Qt
import sqlite3


# Модель данных для отображения задач в таблице
class TaskModel(QAbstractTableModel):
    def __init__(self, tasks=None):
        super().__init__()
        self.tasks = tasks if tasks else []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.tasks)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 7  # 7 колонок: ID, Название, Описание, Категория, Приоритет, Дедлайн, Статус

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            task = self.tasks[index.row()]
            column = index.column()
            if column == 0:
                return task["id"]
            elif column == 1:
                return task["title"]
            elif column == 2:
                return task["description"]
            elif column == 3:
                return task["category"]
            elif column == 4:
                return task["priority"]
            elif column == 5:
                return task["deadline"]
            elif column == 6:
                return task["status"]
        return None

    def update_tasks(self, tasks):
        self.beginResetModel()
        self.tasks = tasks
        self.endResetModel()


# Диалог для добавления / редактирования задачи
class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)

        self.task = task
        self.setWindowTitle("Добавить / Редактировать задачу")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        self.titleEdit = QLineEdit()
        self.titleEdit.setPlaceholderText("Введите название задачи")
        if task:
            self.titleEdit.setText(task["title"])
        layout.addWidget(QLabel("Название задачи:"))
        layout.addWidget(self.titleEdit)

        self.descEdit = QTextEdit()
        if task:
            self.descEdit.setText(task["description"])
        layout.addWidget(QLabel("Описание задачи:"))
        layout.addWidget(self.descEdit)

        self.categoryBox = QComboBox()
        self.categoryBox.addItems(["Работа", "Личное", "Учёба", "Другие"])
        if task:
            self.categoryBox.setCurrentText(task["category"])
        layout.addWidget(QLabel("Категория задачи:"))
        layout.addWidget(self.categoryBox)

        self.priorityBox = QComboBox()
        self.priorityBox.addItems(["Низкий", "Средний", "Высокий"])
        if task:
            self.priorityBox.setCurrentText(task["priority"])
        layout.addWidget(QLabel("Приоритет задачи:"))
        layout.addWidget(self.priorityBox)

        self.deadlineDate = QDateEdit(QDate.currentDate())
        if task:
            self.deadlineDate.setDate(QDate.fromString(task["deadline"], "yyyy-MM-dd"))
        self.deadlineDate.setCalendarPopup(True)
        layout.addWidget(QLabel("Дедлайн задачи:"))
        layout.addWidget(self.deadlineDate)

        self.statusBox = QComboBox()
        self.statusBox.addItems(["В процессе", "Завершена", "Отложена"])
        if task:
            self.statusBox.setCurrentText(task["status"])
        layout.addWidget(QLabel("Статус задачи:"))
        layout.addWidget(self.statusBox)

        buttonBox = QDialogButtonBox()
        buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def get_data(self):
        return {
            "title": self.titleEdit.text(),
            "description": self.descEdit.toPlainText(),
            "category": self.categoryBox.currentText(),
            "priority": self.priorityBox.currentText(),
            "deadline": self.deadlineDate.date().toString("yyyy-MM-dd"),
            "status": self.statusBox.currentText(),
            "created_at": QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        }

    def save_task(self, task_id=None):
        task_data = self.get_data()

        # Подключаемся к базе данных и добавляем или обновляем задачу
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        if task_id:
            # Обновляем задачу
            cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, category = ?, priority = ?, deadline = ?, status = ?, created_at = ?
                WHERE id = ?
            ''', (task_data["title"], task_data["description"], task_data["category"],
                  task_data["priority"], task_data["deadline"], task_data["status"],
                  task_data["created_at"], task_id))
        else:
            # Вставляем новую задачу
            cursor.execute('''
                INSERT INTO tasks (title, description, category, priority, deadline, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (task_data["title"], task_data["description"], task_data["category"],
                  task_data["priority"], task_data["deadline"], task_data["status"],
                  task_data["created_at"]))

        conn.commit()
        conn.close()

    def accept(self):
        task_id = self.task["id"] if self.task else None
        self.save_task(task_id)
        super().accept()


# Главное окно
class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Менеджер задач")
        self.setGeometry(100, 100, 800, 600)

        # Таблица для отображения задач
        self.tableView = QTableView(self)
        self.tableView.setGeometry(50, 50, 700, 400)

        # Кнопка для добавления задачи
        self.addButton = QPushButton("Добавить задачу", self)
        self.addButton.setGeometry(50, 470, 200, 40)
        self.addButton.clicked.connect(self.show_task_dialog)

        # Кнопка для редактирования задачи
        self.editButton = QPushButton("Редактировать задачу", self)
        self.editButton.setGeometry(260, 470, 200, 40)
        self.editButton.clicked.connect(self.show_edit_task_dialog)

        # Кнопка для удаления задачи
        self.deleteButton = QPushButton("Удалить задачу", self)
        self.deleteButton.setGeometry(470, 470, 200, 40)
        self.deleteButton.clicked.connect(self.delete_task)

        # Загрузка данных из базы
        self.load_tasks()

    def load_tasks(self, filter_status=None, filter_keyword=None, filter_category=None):
        # Получаем все задачи из базы данных с фильтром
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM tasks WHERE 1=1'

        if filter_status:
            query += ' AND status = ?'
        if filter_keyword:
            query += ' AND (title LIKE ? OR description LIKE ?)'
        if filter_category:
            query += ' AND category = ?'

        cursor.execute(query, tuple(
            [filter_status] if filter_status else [] +
                                                  [f'%{filter_keyword}%'] * 2 if filter_keyword else [] +
                                                                                                     [
                                                                                                         filter_category] if filter_category else []
        ))

        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "priority": row[4],
                "deadline": row[5],
                "status": row[6],
            }
            tasks.append(task)

        conn.close()

        # Обновляем модель таблицы
        self.model = TaskModel(tasks)
        self.tableView.setModel(self.model)

    def show_task_dialog(self):
        # Показать диалог для добавления новой задачи
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Обновить таблицу после добавления задачи
            self.load_tasks()

    def show_edit_task_dialog(self):
        selected_row = self.tableView.selectionModel().selectedRows()
        if selected_row:
            task_id = self.model.tasks[selected_row[0].row()]["id"]
            dialog = TaskDialog(self, task=self.model.tasks[selected_row[0].row()])
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_tasks()

    def delete_task(self):
        selected_row = self.tableView.selectionModel().selectedRows()
        if selected_row:
            task_id = self.model.tasks[selected_row[0].row()]["id"]
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.load_tasks()


# Запуск приложения
def main():
    app = QtWidgets.QApplication([])

    # Главное окно
    window = TaskManager()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
