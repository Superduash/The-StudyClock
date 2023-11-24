import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from plyer import notification
import sqlite3


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

    def add_task(self, task_text):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT MAX(row_id) FROM todo_list')
        row_count = self.c.fetchone()[0] or 0
        data_to_insert = [(task_text, row_count + 1)]
        insert_query = "INSERT INTO todo_list (list_item, row_id) VALUES (?, ?)"
        self.c.executemany(insert_query, data_to_insert)
        self.conn.commit()

    def delete_task(self, row_id):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM todo_list WHERE row_id = ?", (row_id,))
        self.conn.commit()
        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/todolistgui.ui", self)
        self.delete_2.clicked.connect(self.delete_task)
        self.Settings.clicked.connect(self.open_settings_dialog)
        self.Create_task.clicked.connect(self.add_task)
        self.graball()
        
    def open_settings_dialog(self):
        settings_dialog = QDialog(self)
        uic.loadUi("ui/todosettings.ui", settings_dialog)
        settings_dialog.exec_()

    def graball(self):
        db_manager = DatabaseManager()
        records = db_manager.fetch_all_tasks()
        db_manager.close_connection()
        self.task_list.clear()

        for record in records:
            task_text, row_id = record
            item = QListWidgetItem()
            checkbox_item = QCheckBox(task_text)
            checkbox_item.row_id = row_id  # Store the row_id in the checkbox item
            item.setSizeHint(checkbox_item.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, checkbox_item)

    def add_task(self):
        task_text = self.task_input.text()

        if task_text:
            db_manager = DatabaseManager()
            db_manager.add_task(task_text)
            db_manager.close_connection()

            item = QListWidgetItem()
            checkbox_item = QCheckBox(task_text)
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
                db_manager = DatabaseManager()
                db_manager.delete_task(clicked_checkbox.row_id)
                db_manager.close_connection()
                self.task_list.takeItem(self.task_list.row(clicked_item))

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QtGui.QIcon("resources/todo.png"))
        self.create_tray_icon()
        #self.minimizeButton.clicked.connect(self.minimize_to_system_tray)
        self.schedule_notifications()
        
    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("resources/todo.png"))
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_window(self):
        self.showNormal()
        self.activateWindow()

    def minimize_to_system_tray(self):
        self.hide()

    def schedule_notifications(self):
        notification_interval = 5 * 60 * 60  # 5 hours in seconds
        QtCore.QTimer.singleShot(notification_interval * 1000, self.send_notification)

    def send_notification(self):
        db_manager = DatabaseManager()
        records = db_manager.fetch_all_tasks()
        db_manager.close_connection()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
