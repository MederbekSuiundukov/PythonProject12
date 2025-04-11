import sys
from PyQt6.QtWidgets import QApplication
from task_manager_window import TaskManagerWindow
from task_manager import TaskManager

def main():
    app = QApplication(sys.argv)

    task_manager = TaskManager()
    window = TaskManagerWindow(task_manager)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
