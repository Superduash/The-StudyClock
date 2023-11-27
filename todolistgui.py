import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from plyer import notification
import sqlite3
from PyQt5.QtCore import QTimer, QDateTime, QSize, QUrl, QThread, pyqtSignal
from PyQt5.QtMultimedia import QSoundEffect

db_manager = None
trash_bin = []

def create_database():
    global db_manager
    conn = sqlite3.connect('task_buddy.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists todo_list(
        list_item text,
        datetime_created text,
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
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def fetch_all_tasks(self):
        self.c.execute('SELECT * FROM todo_list')
        records = self.c.fetchall()
        return records

    def fetch_all_completed_tasks(self):
        self.c.execute('SELECT * FROM completed_tasks')
        return self.c.fetchall()

    def add_task(self, task_text):
        current_datetime = QDateTime.currentDateTime()
        creation_date = current_datetime.toString("yyyy-MM-dd hh:mm:ss")

        self.c.execute('SELECT MAX(row_id) FROM todo_list')
        row_count = self.c.fetchone()[0] or 0
        data_to_insert = [(task_text, creation_date, row_count + 1)]
        insert_query = "INSERT INTO todo_list (list_item, datetime_created, row_id) VALUES (?, ?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def add_completed_task(self, task_text, date_of_completion, time_of_completion, row_id):
        data_to_insert = [(task_text, date_of_completion, time_of_completion, row_id)]
        insert_query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def delete_task(self, row_id):
        self.c.execute("DELETE FROM todo_list WHERE row_id = ?", (row_id,))
        self.conn.commit()

    def clear_completed_tasks(self):
        completed_tasks = self.fetch_all_completed_tasks()
        trash_bin.extend(completed_tasks)

        self.c.execute("DELETE FROM completed_tasks")
        self.conn.commit()

    def undo_clear_completed_tasks(self):
        for task_data in trash_bin:
            insert_query = "INSERT INTO completed_tasks (task, date_of_completion, time_of_completion, row_id) VALUES (?, ?, ?, ?)"
            self.c.executemany(insert_query, [task_data])
        trash_bin.clear()

        self.conn.commit()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, task_list, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Task Buddy")
        menu = QMenu(parent)
        restore_action = menu.addAction("Restore")
        minimize_action = menu.addAction("Minimize")
        exit_action = menu.addAction("Exit")
        restore_action.triggered.connect(self.restore_app)
        minimize_action.triggered.connect(self.minimize_app)
        exit_action.triggered.connect(self.exit_app)
        self.setContextMenu(menu)

    def restore_app(self):
        app.setActiveWindow(window)
        window.showNormal()

    def minimize_app(self):
        window.hide()

    def show_settings_dialog(self, task_list):
        try:
            selected_item = task_list.currentItem()
            if selected_item:
                settings_dialog = TaskInfoDialog(self, selected_item)
                settings_dialog.exec_()

        except Exception as e:
            QMessageBox.critical(window, 'Error', f'An error occurred while showing task information: {str(e)}')

    def exit_app(self):
        app.quit()
class TaskInfoDialog(QDialog):
    def __init__(self, ui_main_window, selected_item, parent=None):
        try:
            super(TaskInfoDialog, self).__init__(parent)
            uic.loadUi("ui/taskinfo.ui", self)

            all_tasks = db_manager.fetch_all_tasks()
            created_date_text = all_tasks[ui_main_window.task_list.row(selected_item)][1]
            created_datetime = QDateTime.fromString(created_date_text, "yyyy-MM-dd hh:mm:ss")

            date_time_label = self.findChild(QLabel, 'createdtime')
            date_time_label.setText(created_datetime.toString("MMMM d, yyyy hh:mm:ss AP"))

        except Exception as e:
            print("Exception Occurred:", e)

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
        self.info.setEnabled(False)
        self.task_list.itemSelectionChanged.connect(self.check_selection)

    def check_selection(self):
        selected_item = self.task_list.currentItem()
        self.info.setEnabled(selected_item is not None)

    def show_settings_dialog(self):
        try:
            selected_item = self.task_list.currentItem()
            if selected_item:
                settings_dialog = TaskInfoDialog(self, selected_item)
                settings_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(window, 'Error', f'An error occurred while showing task information: {str(e)}')

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
            table.setColumnCount(3)

            table.setSelectionBehavior(QAbstractItemView.SelectRows)

            for row, task_data in enumerate(completed_tasks):
                for col, value in enumerate(task_data[:-1]):
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
        if row_id is not None and clicked_checkbox.isChecked():
            db_manager.add_completed_task(task, deletion_date, deletion_time, row_id)
            db_manager.delete_task(row_id)
            self.refresh_ongoing_tasks()

    def graball(self):
        records = db_manager.fetch_all_tasks()
        self.task_list.clear()

        for record in records:
            if len(record) == 3:
                task_text, created_date, row_id = record
                item = QListWidgetItem()
                checkbox_item = QCheckBox(task_text)
                checkbox_item.clicked.connect(lambda _, checkbox_item=checkbox_item: self.checkbox_clicked(checkbox_item))
                checkbox_item.row_id = row_id
                item.setSizeHint(checkbox_item.sizeHint())
                self.task_list.addItem(item)
                self.task_list.setItemWidget(item, checkbox_item)
                item.setSizeHint(QSize(item.sizeHint().width(), 35))

    def add_task(self):
        try:
            task_text = self.task_input.text()

            if task_text:
                db_manager.add_task(task_text)
                item = QListWidgetItem()
                checkbox_item = QCheckBox(task_text)
                checkbox_item.clicked.connect(lambda _, checkbox_item=checkbox_item: self.checkbox_clicked(checkbox_item))
                checkbox_item.row_id = db_manager.fetch_all_tasks()[-1][2]
                item.setSizeHint(checkbox_item.sizeHint())
                self.task_list.addItem(item)
                self.task_list.setItemWidget(item, checkbox_item)
                self.task_input.clear()

                self.graball()

        except Exception as e:
            QMessageBox.critical(window, 'Error', f'An error occurred while adding the task: {str(e)}')

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

class NotificationThread(QThread):
    notify_signal = pyqtSignal()

    def run(self):
        self.notify_signal.emit()

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QtGui.QIcon("resources/todo.png"))
        self.schedule_notifications()
        self.tray_icon = SystemTrayIcon(QtGui.QIcon("resources/todo.png"), self.task_list, self)
        self.tray_icon.show()
        self.notification_sound = QSoundEffect()
        self.notification_sound.setSource(QUrl.fromLocalFile("resources/notify.wav"))
        self.notification_thread = NotificationThread()
        self.notification_thread.notify_signal.connect(self.send_notification_and_reschedule)

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
        QTimer.singleShot(notification_interval * 1000, self.send_notification_and_reschedule)
        QTimer.singleShot(notification_interval * 1000, self.schedule_notifications)

    def send_notification_and_reschedule(self):
        self.send_notification()
        self.schedule_notifications()

    def send_notification(self):
        records = db_manager.fetch_all_tasks()
        if records:
            try:
                notification.notify(
                    title="Reminder",
                    message="Don't forget to check your ongoing tasks!",
                    timeout=10,
                )
                self.notification_sound.play()
            except Exception as e:
                print(f"Notification error: {e}")

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
