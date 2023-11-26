import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import timedelta, datetime
from plyer import notification
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/studyfocus.ui", self)
        MainWindow.setFixedSize(MainWindow.size())  # Set fixed size
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)  # Keep close and minimize buttons
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.simple.clicked.connect(self.simplelevel)
        self.medium.clicked.connect(self.mediumlevel)
        self.intense.clicked.connect(self.intenselevel)
        self.custom.clicked.connect(self.customlevel)
        self.minimize.clicked.connect(self.minimize_to_system_tray)
        self.reset.clicked.connect(self.reset_timer)
        self.start.clicked.connect(self.start_timer)
        self.paused = False
        self.elapsed_time = 0
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QtGui.QIcon("resources/todo.png"))

    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()     
    def start_timer(self):
        if self.timer == "00:00:00":
            msg = QMessageBox()
            msg.setText("You didn't select a mode")
        else:
            if not self.timer.isActive() and not self.paused:
                self.start_time = datetime.now()
                self.timer.start(20) 
                self.start.setEnabled(False) 
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_timer) 
    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        text = self.mode.text()
        if text == "Simple":
            self.timer = QLabel(self)
            self.timer.setText("01:00:00")
        elif text == "Medium":
            self.timer = QLabel(self)
            self.timer.setText("02:00:00")
        elif text == "Intense":
            self.timer = QLabel(self)
            self.timer.setText("03:00:00")
        elif text == "Custom":
           self.start_button.setEnabled(True)
           self.paused = False
    def pause_resume_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.paused = True
            self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
        else:
            if self.paused:
                self.start_time = datetime.now()
                self.timer.start(20)
                self.paused = False
            else:
                self.start_time = datetime.now()
                self.timer.start(20)
                self.paused = False
                self.start.setEnabled(False)
    def show_notification(self):
        if not self.notification_shown:
            self.play_sound(self.notify_sound)
            notification.notify(
                title="20-20-20 Rule Reminder",
                message="Session up.. Time for a short break",
                timeout=5,
            )
            self.delay_timer.start(25 * 1000)
            self.notification_shown = True
    def reset_timer(self):
        self.timer.setText("00:00:00")
    def simplelevel(self):
            self.timer.setText("01:00:00")
            self.mode.setText("Simple")
    def mediumlevel(self):
        self.timer.setText("02:00:00")
        self.mode.setText("Medium")
    def intenselevel(self):
        self.timer.setText("03:00:00")
        self.mode.setText("Intense")
    def customlevel(self):
        self.mode.setText("Custom")
        self.customwindow = QMainWindow()
        uic.loadUi("ui/studyfocuscustom.ui", self.customwindow)
        self.customwindow.show()
    def update_timer(self):
        if self.start_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            remaining_time = self.timer_duration.total_seconds() - elapsed_time

            if remaining_time <= 0:
                self.show_notification()
            else:
                minutes, seconds = divmod(int(remaining_time), 60)
                formatted_time = f"{minutes:02d}:{seconds:02d}"
                self.timer.setText(formatted_time)

    def minimize_to_system_tray(self):
        self.hide()
        self.create_system_tray_icon()
    def create_system_tray_icon(self):
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/logo.jpg"))
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
    def close_application(self):
        self.tray_icon.hide()
        sys.exit()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
