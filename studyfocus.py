import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
        
    def customlevel(self):
        self.mode.setText("Custom")
        self.customwindow = QMainWindow()
        uic.loadUi("ui/studyfocuscustom.ui", self.customwindow)
        self.custom_timer_window()
        self.customwindow.show()
        
    def custom_timer_window(self):
        done_button = self.customwindow.findChild(QPushButton, 'save')
        self.length_of_session1 = self.customwindow.findChild(QTimeEdit, 'length_of_session')
        self.length_of_break1 = self.customwindow.findChild(QTimeEdit, 'length_of_break')
        done_button.clicked.connect(self.customaddons)
        
    def customaddons(self):
        self.selected_time = self.length_of_session1.time()
        self.time_in_seconds = (-1)* self.selected_time.secsTo(QTime(0, 0))
        self.formatted_time = self.selected_time.toString("hh:mm:ss")
        self.timer_label.setText(self.formatted_time)
        self.selected_break_time = self.length_of_break1.time()
        self.break_time_in_seconds = (-1)* self.selected_break_time.secsTo(QTime(0, 0))
        self.formatted_break_time = self.selected_break_time.toString("hh:mm:ss")

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
        self.pause.clicked.connect(self.pause_resume_timer)
        
        self.notify_sound = QSoundEffect()
        self.notify_sound.setSource(QUrl.fromLocalFile("resources/notify.wav"))
        
        self.notification_shown = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        self.break_timer = QTimer(self)
        self.break_timer.timeout.connect(self.update_break_timer)
        
    def start_timer(self):
        if self.timer_label.text() == "00:00:00":
            # Display a QMessageBox indicating that a mode needs to be selected
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please select a mode before starting the timer.")
            msg.setWindowTitle("Mode Not Selected!!")
            msg.exec_()
        elif self.mode.text() in ["Simple", "Medium", "Intense","Custom"]:
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
                self.timer.stop()
                self.pause.clicked.disconnect(self.pause_resume_timer)
                self.pause.clicked.connect(self.break_pause_resume_timer)
                notification.notify(
                title="Break Time!!",
                message="It's break time! Take a break!",
                timeout=5,
                )  
                self.play_sound(self.notify_sound)
                mode_text = self.mode.text()
                if mode_text == "Simple":
                    self.timer_label.setText("00:00:15")
                elif mode_text == "Medium":
                    self.timer_label.setText("00:20:00")    
                elif mode_text == "Intense":
                    self.timer_label.setText("00:30:00")
                elif mode_text == "Custom":
                    self.timer_label.setText(self.formatted_break_time)
                self.break_time = datetime.now()
                self.elapsed_time = 0
                self.break_time_duration = self.get_break_timer_duration()
                self.break_timer.start(50)
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
                
            else:
                hours= int(remaining_time//3600)
                minutes = int(remaining_time//60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)
    def update_break_timer(self):
        if self.break_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.break_time).total_seconds()
            remaining_time = self.break_time_duration.total_seconds() - elapsed_time
            
            if remaining_time <= 0:
                self.break_timer.stop()
                self.pause.clicked.disconnect(self.break_pause_resume_timer)
                self.pause.clicked.connect(self.pause_resume_timer)
                notification.notify(
                title="Break Ended",
                message="Break is over! Time for another study session!",
                timeout=5,
                )  
                self.play_sound(self.notify_sound)
                mode_text = self.mode.text()
                if mode_text == "Simple":
                    self.timer_label.setText("00:30:00")
                elif mode_text == "Medium":
                    self.timer_label.setText("02:00:00")    
                elif mode_text == "Intense":
                    self.timer_label.setText("03:00:00")
                elif mode_text == "Custom":
                    self.timer_label.setText(self.formatted_time)
                self.start_time = datetime.now()
                self.elapsed_time = 0
                self.timer_duration = self.get_timer_duration()
                self.timer.start(20)
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
            else:
                hours= int(remaining_time//3600)
                minutes = int(remaining_time//60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)
                
            
        
    def get_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(seconds=30)
        elif mode_text == "Medium":
            return timedelta(hours=2)
        elif mode_text == "Intense":
            return timedelta(hours=3)
        elif mode_text == "Custom":
             return timedelta(seconds=self.time_in_seconds)
        else:
            return timedelta()
    def get_break_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(seconds=15)
        elif mode_text == "Medium":
            return timedelta(minutes=20)
        elif mode_text == "Intense":
            return timedelta(minutes=30)
        elif mode_text == "Custom":
            return timedelta(seconds=self.break_time_in_seconds)
        else:
            return timedelta()
    def simplelevel(self):
        self.timer_label.setText("00:00:30")
        self.mode.setText("Simple")

    def mediumlevel(self):
        self.timer_label.setText("02:00:00")
        self.mode.setText("Medium")

    def intenselevel(self):
        self.timer_label.setText("03:00:00")
        self.mode.setText("Intense")

        
          
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
            self.timer_label.setText(self.formatted_time)
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
    def break_pause_resume_timer(self):
        if self.break_timer.isActive():
            self.break_timer.stop()
            self.paused = True
            self.elapsed_time += (datetime.now() - self.break_time).total_seconds()
        else:
            if self.paused:
                self.break_time = datetime.now()
                self.break_timer.start(20)
                self.paused = False
            else:
                self.break_time = datetime.now()
                self.break_timer.start(20)
                self.paused = False
                self.start.setEnabled(False)
    def minimize_to_system_tray(self):
        self.hide()
        if not hasattr(self, 'tray_icon'):
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
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        sys.exit()

    def play_sound(self, sound_effect):
        if sound_effect.isLoaded():
            sound_effect.play()
        else:
            print("Error: Sound file not loaded.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
    
'''QtCore.QTimer.singleShot(1000, self.show_break_notification)  92 
self.show_notification("Break Started", "Enjoy your break!", self.break_duration) 99
self.show_notification("Break Ended", "Time for another study session!", self.timer_duration)'''