import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QTimeEdit, QMessageBox
from PyQt5.QtCore import Qt, QTime
from PyQt5 import QtGui


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.loadTasks()

    def initUI(self):
        self.setWindowTitle('Daily Task Manager')
        self.setGeometry(100, 100, 600, 300)

        self.tasks_table = QTableWidget(self)
        self.tasks_table.setColumnCount(3)
        self.tasks_table.setHorizontalHeaderLabels(
            ['Task', 'Due Time', 'Priority'])

        self.task_input = QLineEdit(self)
        self.due_time_input = QTimeEdit(self)
        self.priority_combobox = QComboBox(self)
        self.priority_combobox.addItems(['High', 'Medium', 'Low'])

        self.add_button = QPushButton('Add Task', self)
        self.remove_button = QPushButton('Remove Task', self)

        self.layoutUI()

    def layoutUI(self):
        v_layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()

        # Apply styles using QSS
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0; /* Set the background color */
            }
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }
            QLineEdit, QTimeEdit, QComboBox {
                background-color: #e0e0e0; /* Light gray */
                border: 1px solid #ccc;
                padding: 5px;
            }
            QTableWidget {
                background-color: #fff; /* White */
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #ddd; /* Light gray for header */
            }
            """)

        v_layout.addWidget(self.tasks_table)
        v_layout.addWidget(self.task_input)
        v_layout.addWidget(self.due_time_input)
        v_layout.addWidget(self.priority_combobox)
        h_layout.addWidget(self.add_button)
        h_layout.addWidget(self.remove_button)
        v_layout.addLayout(h_layout)

        self.add_button.clicked.connect(self.addTask)
        self.remove_button.clicked.connect(self.removeTask)

        self.show()

    def addTask(self):
        task_text = self.task_input.text().strip()
        due_time = self.due_time_input.time().toString("hh:mm")
        priority = self.priority_combobox.currentText()

        if task_text:
            row_position = self.tasks_table.rowCount()
            self.tasks_table.insertRow(row_position)
            self.tasks_table.setItem(
                row_position, 0, QTableWidgetItem(task_text))
            self.tasks_table.setItem(
                row_position, 1, QTableWidgetItem(due_time))

            # Set the priority item with color coding
            priority_item = QTableWidgetItem(priority)
            priority_item.setBackground(self.getPriorityColor(priority))
            self.tasks_table.setItem(row_position, 2, priority_item)

            self.task_input.clear()
            self.due_time_input.clear()
            self.priority_combobox.setCurrentIndex(0)

            self.saveTasks()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a task.')

    def removeTask(self):
        selected_rows = set(
            index.row() for index in self.tasks_table.selectionModel().selectedIndexes())

        for row in sorted(selected_rows, reverse=True):
            self.tasks_table.removeRow(row)

        self.saveTasks()

    def saveTasks(self):
        with open('tasks.txt', 'w') as file:
            for row in range(self.tasks_table.rowCount()):
                task = self.tasks_table.item(row, 0).text()
                due_time = self.tasks_table.item(row, 1).text()
                priority = self.tasks_table.item(row, 2).text()
                file.write(f"{task},{due_time},{priority}\n")

    def loadTasks(self):
        try:
            with open('tasks.txt', 'r') as file:
                tasks = [line.strip().split(',') for line in file.readlines()]
                self.tasks_table.setRowCount(len(tasks))

                for row, task in enumerate(tasks):
                    self.tasks_table.setItem(row, 0, QTableWidgetItem(task[0]))
                    self.tasks_table.setItem(row, 1, QTableWidgetItem(task[1]))

                # Set the priority item with color coding
                    priority_item = QTableWidgetItem(task[2])
                    priority_item.setBackground(self.getPriorityColor(task[2]))
                    self.tasks_table.setItem(row, 2, priority_item)

        except FileNotFoundError:
            pass

    def getPriorityColor(self, priority):
        color_dict = {'High': '#4CAF50', 'Medium': '#FFD700', 'Low': '#FF0000'}
        # Default to white if not found
        color = color_dict.get(priority, '#FFFFFF')

        # Create a QBrush with the desired color
        brush = QtGui.QBrush(QtGui.QColor(color))

        return brush


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    sys.exit(app.exec_())
