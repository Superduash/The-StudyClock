import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from plyer import notification
import sqlite3
from PyQt5.QtCore import QTimer, QDateTime, Qt
from datetime import datetime, timedelta

db_manager = None
trash_bin = []


def create_database():
    global db_manager
    conn = sqlite3.connect('task_buddy.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists todo_list(
        list_item text,
        row_id int,
        due_datetime text
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


def send_notification(task_text, timing):
    notification_title = "Reminder"
    notification_message = f"Don't forget to finish '{task_text}' {timing}!"
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_icon="resources/todo.png",
        timeout=10,
    )
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

    def add_task(self, task_text, due_datetime):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT MAX(row_id) FROM todo_list')
        row_count = self.c.fetchone()[0] or 0
        data_to_insert = [(task_text, row_count + 1, due_datetime)]
        insert_query = "INSERT INTO todo_list (list_item, row_id, due_datetime) VALUES (?, ?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def add_completed_task(self, task_text, date_of_completion, time_of_completion, row_id):
        data_to_insert = [(task_text, date_of_completion, time_of_completion, row_id)]
        insert_query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def delete_task(self, row_id):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM todo_list WHERE row_id = ?", (row_id,))
        self.conn.commit()

    def clear_completed_tasks(self):
        completed_tasks = self.fetch_all_completed_tasks()
        trash_bin.extend(completed_tasks)

        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM completed_tasks")
        self.conn.commit()

    def undo_clear_completed_tasks(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        for task_data in trash_bin:
            insert_query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
            self.c.executemany(insert_query, [task_data])
        trash_bin.clear()

        self.conn.commit()

    def update_task_due_datetime(self, task_text, due_datetime, row_id):
        update_query = "UPDATE todo_list SET due_datetime = ? WHERE list_item = ? AND row_id = ?"
        self.c.execute(update_query, (due_datetime, task_text, row_id))
        self.conn.commit()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Task Buddy")
        menu = QMenu(parent)
        restore_action = menu.addAction("Restore")
        minimize_action = menu.addAction("Minimize")
        settings_action = menu.addAction("Settings")
        exit_action = menu.addAction("Exit")
        restore_action.triggered.connect(self.restore_app)
        minimize_action.triggered.connect(self.minimize_app)
        settings_action.triggered.connect(self.show_settings_dialog)
        exit_action.triggered.connect(self.exit_app)
        self.setContextMenu(menu)

    def restore_app(self):
        app.setActiveWindow(window)
        window.showNormal()

    def minimize_app(self):
        window.hide()

    def show_settings_dialog(self):
        selected_items = window.task_list.selectedItems()
        if selected_items:
            settings_dialog = SettingsDialog()
            settings_dialog.exec_()
        else:
            QMessageBox.warning(window, "Warning", "Please select a task first.")

    def exit_app(self):
        app.quit()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        uic.loadUi("ui/taskinfo.ui", self)

        # Connect buttons to functions
        self.save.clicked.connect(self.save_settings)
        self.cancel.clicked.connect(self.close)

    def save_settings(self):
        try:
            due_datetime = self.setdate.dateTime().toPyDateTime()
            task_text = "Task Name"  # Replace this with the actual task name
            row_id = 1  # Replace this with the actual row_id of the selected task

            # Update the due datetime in the database
            db_manager.update_task_due_datetime(task_text, due_datetime, row_id)

            # Schedule notifications
            self.schedule_notifications(due_datetime, task_text)

            self.close()
        except Exception as e:
            print("Error in save_settings:", str(e))

    def schedule_notifications(self, due_datetime, task_text):
        # Schedule notification 1 day before
        notification_datetime_1_day_before = due_datetime - timedelta(days=1)
        notification_interval_1_day_before = (notification_datetime_1_day_before - datetime.now()).seconds
        QTimer.singleShot(notification_interval_1_day_before * 1000, lambda: send_notification(task_text, "1 day before"))

        # Schedule notification 1 hour before
        notification_datetime_1_hour_before = due_datetime - timedelta(hours=1)
        notification_interval_1_hour_before = (notification_datetime_1_hour_before - datetime.now()).seconds
        QTimer.singleShot(notification_interval_1_hour_before * 1000, lambda: send_notification(task_text, "1 hour before"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/todolistgui.ui", self)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.delete_2.clicked.connect(self.delete_task)
        self.minimize.clicked.connect(self.minimize_to_tray)
        self.Create_task.clicked.connect(self.add_task)
        self.Completed.clicked.connect(self.open_completed_tasks)
        self.refresh_2.clicked.connect(self.refresh_ongoing_tasks)
        self.info.clicked.connect(self.show_settings_dialog)
        self.graball()

    def show_settings_dialog(self):
        try:
            selected_item = self.task_list.currentItem()
            if selected_item:
                settings_dialog = SettingsDialog(self)
                settings_dialog.exec_()
        except Exception as e:
            print("Error in show_settings_dialog:", str(e))

    def open_completed_tasks(self):
        self.completedwindow = QMainWindow()
        uic.loadUi("ui/finishedassignments.ui", self.completedwindow)
        self.completedwindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        self.completedwindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.completed_tasks_table()
        self.completedwindow.show()

    def completed_tasks_table(self):
        completed_tasks = db_manager.fetch_all_completed_tasks()
        table = self.completedwindow.findChild(QTableWidget, 'complete_table')

        if table:
            table.setRowCount(len(completed_tasks))
            table.setColumnCount(4)  # Changed to 4 columns

            # Hide the new column (due_datetime)
            table.setColumnHidden(3, True)

            table.setSelectionBehavior(QAbstractItemView.SelectRows)

            for row, task_data in enumerate(completed_tasks):
                for col, value in enumerate(task_data):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)
                    if col == 2:
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            refresh_button = self.completedwindow.findChild(QPushButton, 'refresh')
            undo_button = self.completedwindow.findChild(QPushButton, 'undo')
            clear_button = self.completedwindow.findChild(QPushButton, 'clear')

            refresh_button.clicked.connect(self.refresh_completed_tasks)
            undo_button.clicked.connect(self.undo_clear_completed_tasks)
            clear_button.clicked.connect(self.clear_completed_tasks)

    def refresh_completed_tasks(self):
        self.completed_tasks_table()

    def clear_completed_tasks(self):
        result = QMessageBox.question(
            self.completedwindow,
            'Confirmation',
            'Are you sure you want to clear completed tasks?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if result == QMessageBox.Yes:
            db_manager.clear_completed_tasks()
            self.completed_tasks_table()

    def undo_clear_completed_tasks(self):
        result = QMessageBox.question(
            self.completedwindow,
            'Confirmation',
            'Are you sure you want to undo clearing completed tasks?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if result == QMessageBox.Yes:
            db_manager.undo_clear_completed_tasks()
            self.completed_tasks_table()

    def minimize_to_tray(self):
        window.hide()
        if hasattr(self, 'completedwindow') and self.completedwindow.isVisible():
            self.completedwindow.hide()

    def checkbox_clicked(self, clicked_checkbox):
        task = clicked_checkbox.text()
        current_datetime = QDateTime.currentDateTime()
        deletion_date = current_datetime.date().toString("yyyy-MM-dd")
        deletion_time = current_datetime.time().toString("hh:mm:ss")
        row_id = getattr(clicked_checkbox, 'row_id', None)
        print(row_id)
        if row_id is not None and clicked_checkbox.isChecked():
            db_manager.add_completed_task(task, deletion_date, deletion_time, row_id)
            db_manager.delete_task(row_id)
            self.refresh_ongoing_tasks()

    def graball(self):
        records = db_manager.fetch_all_tasks()
        self.task_list.clear()

        for record in records:
            if len(record) >= 2:
                task_text, row_id = record[:2]
                item = QListWidgetItem()
                checkbox_item = QCheckBox(task_text)
                checkbox_item.clicked.connect(lambda _, checkbox_item=checkbox_item: self.checkbox_clicked(checkbox_item))
                checkbox_item.row_id = row_id
                item.setSizeHint(checkbox_item.sizeHint())
                self.task_list.addItem(item)
                self.task_list.setItemWidget(item, checkbox_item)


    def add_task(self):
        task_text = self.task_input.text()

        if task_text:
            due_datetime = QDateTime.currentDateTime().addDays(1)  # Default due datetime is 1 day from now
            db_manager.add_task(task_text, due_datetime.toString(Qt.ISODate))
            item = QListWidgetItem()
            checkbox_item = QCheckBox(task_text)
            checkbox_item.clicked.connect(lambda _, checkbox_item=checkbox_item: self.checkbox_clicked(checkbox_item))
            checkbox_item.row_id = db_manager.fetch_all_tasks()[-1][1]
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

    def refresh_ongoing_tasks(self):
        self.graball()


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QtGui.QIcon("resources/todo.png"))
        self.schedule_notifications()
        self.tray_icon = SystemTrayIcon(QtGui.QIcon("resources/todo.png"), self)
        self.tray_icon.show()

    def minimize_app(self):
        self.hide()
        if hasattr(self, 'completedwindow') and self.completedwindow.isVisible():
            self.completedwindow.hide()

    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    def schedule_notifications(self):
        notification_interval = 5 * 60 * 60
        QTimer.singleShot(notification_interval * 1000, send_notification)


if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
