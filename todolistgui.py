import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from plyer import notification
import sqlite3
from PyQt5.QtCore import QTimer, QDateTime

db_manager = None

def create_database():
    global db_manager
    conn = sqlite3.connect('task_buddy.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists todo_list(
        list_item text,
        row_id int
        )""")
    c.execute("""CREATE TABLE if not exists completed_tasks(
        task text,
        date_of_completion text,
        time_of_completion text,
        row_id int
        )""")
    conn.commit()
    conn.close()

    db_manager = DatabaseManager()

def send_notification():
    records = db_manager.fetch_all_tasks()
    if records:
        notification_title = "Reminder"
        notification_message = "Don't forget to check your tasks!"
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon="resources/todo.png",
            timeout=10,
        )
        # Play notification sound
        QtGui.QSound("resources/notify.wav").play()

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def fetch_all_tasks(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM todo_list')
        return self.c.fetchall()

    def fetch_all_completed_tasks(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM completed_tasks')
        return self.c.fetchall()

    def add_task(self, task_text):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT MAX(row_id) FROM todo_list')
        row_count = self.c.fetchone()[0] or 0
        data_to_insert = [(task_text, row_count + 1)]
        insert_query = "INSERT INTO todo_list (list_item, row_id) VALUES (?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def add_completed_task(self, task_text, date_of_completion, time_of_completion, row_id):
        data_to_insert = [(task_text, date_of_completion, time_of_completion, row_id)]
        insert_query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def delete_task(self, row_id):
        try:
            self.conn = sqlite3.connect('task_buddy.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE FROM todo_list WHERE row_id = ?", (row_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting task: {e}")

    def delete_completed_task(self, row_id):
        try:
            self.conn = sqlite3.connect('task_buddy.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE FROM completed_tasks WHERE row_id = ?", (row_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting completed task: {e}")

    def clear_completed_tasks(self):
        try:
            self.conn = sqlite3.connect('task_buddy.db')
            self.c = self.conn.cursor()
            self.c.execute("DELETE FROM completed_tasks")
            self.conn.commit()
        except Exception as e:
            print(f"Error clearing completed tasks: {e}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/todolistgui.ui", self)
        MainWindow.setFixedSize(MainWindow.size())  # Set fixed size
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)  # Keep close and minimize buttons
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)  # Disable maximize button
        self.delete_2.clicked.connect(self.delete_task)
        self.Settings_2.clicked.connect(self.open_settings_dialog)
        self.Create_task.clicked.connect(self.add_task)
        self.Completed.clicked.connect(self.open_completed_tasks)
        self.graball()

    def open_settings_dialog(self):
        self.todosettings = QDialog()
        uic.loadUi("ui/todosettings.ui", self.todosettings)
        self.todosettings.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)  # Keep close and minimize buttons
        self.todosettings.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)  # Disable maximize button
        self.todosettings.show()

    def open_completed_tasks(self):
        self.completedwindow = QMainWindow()
        uic.loadUi("ui/finishedassignments.ui", self.completedwindow)
        self.completedwindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)  # Keep close and minimize buttons
        self.completedwindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)  # Disable maximize button
        self.completed_tasks_table()
        self.completedwindow.show()

    def completed_tasks_table(self):
        completed_tasks = db_manager.fetch_all_completed_tasks()
        table = self.completedwindow.findChild(QTableWidget, 'complete_table')

        if table:
            table.setRowCount(len(completed_tasks))
            table.setColumnCount(4)  # Assuming there are four columns in your table

            # Set the selection behavior to select entire rows
            table.setSelectionBehavior(QAbstractItemView.SelectRows)

            for row, task_data in enumerate(completed_tasks):
                for col, value in enumerate(task_data):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)
                    if col == 3:
                        item.row_id = int(value)

            refresh_button = self.completedwindow.findChild(QPushButton, 'refresh')
            restore_button = self.completedwindow.findChild(QPushButton, 'restore')
            delete_button = self.completedwindow.findChild(QPushButton, 'delete_2')
            clear_button = self.completedwindow.findChild(QPushButton, 'clear')

            refresh_button.clicked.connect(self.refresh_completed_tasks)
            restore_button.clicked.connect(self.restore_completed_task)
            delete_button.clicked.connect(self.delete_completed_task)
            clear_button.clicked.connect(self.clear_completed_tasks)

    # Modify the delete_completed_task method in Ui_MainWindow class
    # Modify the delete_completed_task method in Ui_MainWindow class
    def delete_completed_task(self):
        table = self.completedwindow.findChild(QTableWidget, 'complete_table')
        selected_rows = set(index.row() for index in table.selectedIndexes())

        # Sort the selected rows in descending order
        selected_rows = sorted(selected_rows, reverse=True)

        for selected_row in selected_rows:
            try:
                row_id_item = table.item(selected_row, 3)  # Assuming row_id is in the fourth column
                if row_id_item:
                    row_id = int(row_id_item.text())
                    print(f"Deleting completed task with ID: {row_id}")
                    db_manager.delete_completed_task(row_id)
            except Exception as e:
                print(f"Error deleting completed task: {e}")

        self.completed_tasks_table()  # Refresh the table after deletion


    def refresh_completed_tasks(self):
        self.completed_tasks_table()

    def restore_completed_task(self):
        table = self.completedwindow.findChild(QTableWidget, 'complete_table')
        selected_row = table.currentRow()

        if selected_row >= 0:
            row_id_item = table.item(selected_row, 3)  # Assuming row_id is in the fourth column
            if row_id_item is not None:
                row_id = int(row_id_item.text())
                task_text_item = table.item(selected_row, 0)  # Assuming task text is in the first column
                if task_text_item is not None:
                    task_text = task_text_item.text()
                    current_datetime = QDateTime.currentDateTime()
                    date_of_completion = current_datetime.date().toString("yyyy-MM-dd")
                    time_of_completion = current_datetime.time().toString("hh:mm:ss")

                    try:
                        # Use a single transaction to delete and insert records
                        db_manager.conn.execute("BEGIN TRANSACTION")
                        db_manager.c.execute("DELETE FROM completed_tasks WHERE row_id = ?", (row_id,))
                        db_manager.add_completed_task(task_text, date_of_completion, time_of_completion, row_id)
                        db_manager.conn.execute("COMMIT")

                        self.completed_tasks_table()
                    except Exception as e:
                        db_manager.conn.execute("ROLLBACK")
                        print(f"Error restoring completed task: {e}")
                else:
                    print("Unable to retrieve task text item.")
            else:
                print("Unable to retrieve row ID item.")

    def clear_completed_tasks(self):
        try:
            # Add logic to clear completed tasks
            db_manager.clear_completed_tasks()
            self.completed_tasks_table()
        except Exception as e:
            print(f"Error clearing completed tasks: {e}")

    def checkbox_clicked(self):
        clicked_checkbox = self.sender()
        task = clicked_checkbox.text()
        current_datetime = QDateTime.currentDateTime()
        deletion_date = current_datetime.date().toString("yyyy-MM-dd")
        deletion_time = current_datetime.time().toString("hh:mm:ss")
        clicked_item = self.task_list.currentRow()
        print(clicked_item)
        if clicked_checkbox.isChecked():
            query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
            data_to_insert = [(task, deletion_date, deletion_time, clicked_item)]
            conn = sqlite3.connect('task_buddy.db')
            c = conn.cursor()
            c.executemany(query, data_to_insert)
            conn.commit()
            conn.close()
            print("success")
            item = self.task_list.itemAt(clicked_checkbox.pos())
            db_manager.delete_task(clicked_checkbox.row_id)
            self.task_list.takeItem(self.task_list.row(item))

    def graball(self):
        records = db_manager.fetch_all_tasks()
        self.task_list.clear()

        for record in records:
            task_text, row_id = record
            item = QListWidgetItem()
            checkbox_item = QCheckBox(task_text)
            checkbox_item.clicked.connect(self.checkbox_clicked)
            checkbox_item.row_id = row_id  # Store the row_id in the checkbox item
            item.setSizeHint(checkbox_item.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, checkbox_item)

    def add_task(self):
        task_text = self.task_input.text()

        if task_text:
            db_manager.add_task(task_text)
            item = QListWidgetItem()
            checkbox_item = QCheckBox(task_text)
            checkbox_item.clicked.connect(self.checkbox_clicked)
            checkbox_item.row_id = db_manager.fetch_all_tasks()[-1][1]  # Fetch the latest row_id
            item.setSizeHint(checkbox_item.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, checkbox_item)
            self.task_input.clear()

    def delete_task(self):
        clicked_item = self.task_list.currentItem()
        if clicked_item is not None:
            result = QMessageBox.question(
                self,
                'Confirmation',
                'Are you sure you want to delete this task?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if result == QMessageBox.Yes:
                clicked_checkbox = self.task_list.itemWidget(clicked_item)
                db_manager.delete_task(clicked_checkbox.row_id)
                self.task_list.takeItem(self.task_list.row(clicked_item))

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QtGui.QIcon("resources/todo.png"))
        self.schedule_notifications()

    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    def schedule_notifications(self):
        notification_interval = 5 * 60 * 60  # 5 hours in seconds
        QTimer.singleShot(notification_interval * 1000, send_notification)

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())