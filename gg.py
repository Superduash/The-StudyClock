import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSystemTrayIcon, QMenu, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime, Qt
from datetime import datetime, timedelta
from plyer import notification
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtMultimedia import QSoundEffect

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/studyfocus.ui", self)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
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
        self.setWindowIcon(QIcon("resources/todo.png"))

        self.start_time = None
        self.elapsed_time = 0
        self.notification_shown = False
        self.notify_sound = "resources/notify.wav"  # Replace with the correct path to your sound file

        # Connect the button click to the appropriate level method
        self.simple.clicked.connect(self.simplelevel)
        self.medium.clicked.connect(self.mediumlevel)
        self.intense.clicked.connect(self.intenselevel)
        self.custom.clicked.connect(self.customlevel)
        self.start.clicked.connect(self.start_timer)
        self.reset.clicked.connect(self.reset_timer)
        self.minimize.clicked.connect(self.minimize_to_system_tray)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
    def start_timer(self):
        if self.timer_label.text() == "00:00:00":
            # Display a QMessageBox indicating that a mode needs to be selected
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please select a mode before starting the timer.")
            msg.setWindowTitle("Mode Not Selected")
            msg.exec_()
        elif self.mode.text() in ["Simple", "Medium", "Intense"]:
            self.start_time = datetime.now()
            self.elapsed_time = 0
            self.timer_duration = self.get_timer_duration()
            self.timer.start(20)
            self.start.setEnabled(False)
            self.paused = False
            self.notification_shown = False

    def update_timer(self):
        if self.start_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            remaining_time = self.timer_duration.total_seconds() - elapsed_time

            if remaining_time <= 0:
                pass
            
            else:
                minutes, seconds = divmod(int(remaining_time), 60)
                formatted_time = f"{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)

    def get_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(seconds=10)
        elif mode_text == "Medium":
            return timedelta(hours=2)
        elif mode_text == "Intense":
            return timedelta(hours=3)
        else:
            return timedelta()
        
    def show_break_notification(self):
        self.show_notification("Break Time", "Take a break!", self.get_break_duration())

    def simplelevel(self):
        self.timer_label.setText("00:00:10")
        self.mode.setText("Simple")

    def mediumlevel(self):
        self.timer_label.setText("02:00:00")
        self.mode.setText("Medium")

    def intenselevel(self):
        self.timer_label.setText("03:00:00")
        self.mode.setText("Intense")

    def customlevel(self):
        self.mode.setText("Custom")
        self.customwindow = QMainWindow()
        uic.loadUi("ui/studyfocuscustom.ui", self.customwindow)
        self.customwindow.show()
    
    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()     
        
    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        text = self.mode.text()
        if text == "Simple":
            self.timer_label.setText("00:00:10")
        elif text == "Medium":
            self.timer_label.setText("02:00:00")
        elif text == "Intense":
            self.timer_label.setText("03:00:00")
        elif text == "Custom":
            # Handle resetting for custom mode (if needed)
            pass
        self.start.setEnabled(True)  # Re-enable the start button
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
        
    def show_notification(self, title, message, timeout):
        notification.notify(
            title=title,
            message=message,
            timeout=5,
        )
    def play_sound(self, sound_path):
        sound_effect = QSoundEffect()
        sound_effect.setSource(QtCore.QUrl.fromLocalFile(sound_path))
        sound_effect.setVolume(1.0)
        sound_effect.play()
    def play_click_sound(self):
        self.play_sound(self.click_sound)
    

    # Your existing code for other methods here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
    
'''QtCore.QTimer.singleShot(1000, self.show_break_notification)  92 
self.show_notification("Break Started", "Enjoy your break!", self.break_duration) 99
self.show_notification("Break Ended", "Time for another study session!", self.timer_duration)'''