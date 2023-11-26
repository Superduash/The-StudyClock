import sys   #importing the modules required
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
        uic.loadUi("ui/studyfocus.ui", self)  #loads the ui file which contains the gui
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False) 
        
        self.custom.clicked.connect(self.customlevel)
        
    def customlevel(self):
        self.mode.setText("Custom")
        self.customwindow = QMainWindow()
        uic.loadUi("ui/studyfocuscustom.ui", self.customwindow) #loads the custom timer ui
        self.custom_timer_window()
        self.customwindow.show()
        
    def custom_timer_window(self):
        done_button = self.customwindow.findChild(QPushButton, 'save') #locates the position of the objects in the custom timer window
        self.length_of_session1 = self.customwindow.findChild(QTimeEdit, 'length_of_session')
        self.length_of_break1 = self.customwindow.findChild(QTimeEdit, 'length_of_break')
        done_button.clicked.connect(self.customaddons)
        
    def customaddons(self):
        self.selected_time = self.length_of_session1.time()
        self.time_in_seconds = (-1)* self.selected_time.secsTo(QTime(0, 0)) #converts time to seconds
        self.formatted_time = self.selected_time.toString("hh:mm:ss")
        self.timer_label.setText(self.formatted_time) #sets the timer label for custom timer
        self.selected_break_time = self.length_of_break1.time()
        self.break_time_in_seconds = (-1)* self.selected_break_time.secsTo(QTime(0, 0))
        self.formatted_break_time = self.selected_break_time.toString("hh:mm:ss")

class MyMainWindow(QMainWindow, Ui_MainWindow):         #new class which is inherited from QMainWindow and Ui_MainWindow
    def __init__(self):                             #constructor method for MyMainWindow
        super().__init__()                       #calls the constructor of the base class 'QMainWindow',performs neccessary setup
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QIcon("resources/todo.png"))

        self.start_time = None
        self.elapsed_time = 0
        self.notification_shown = False
        self.notify_sound = "resources/notify.wav"  #needed to play the notification audio

        #assigning the buttons their respective functions
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

        self.timer = QTimer(self) #assiging a variable which will act as the timer variable
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
        elif self.mode.text() in ["Simple", "Medium", "Intense","Custom"]: #checks if the mode is selected 
            self.start_time = datetime.now()
            self.elapsed_time = 0
            self.timer_duration = self.get_timer_duration()
            self.timer.start(20) #starts timer
            self.start.setEnabled(False)
            self.paused = False
            self.notification_shown = False

    def update_timer(self):
        if self.start_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            remaining_time = self.timer_duration.total_seconds() - elapsed_time 

            if remaining_time <= 0: #indicates that the session time is over and it will start the break time
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
                if mode_text == "Simple":         #changes the label to the respective break times
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
                self.break_timer.start(50) #starts the break time 
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
                
            else:
                hours= int(remaining_time//3600)       
                minutes = int(remaining_time//60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time) #Sets the time to the label each second which passes by
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
                if mode_text == "Simple":            #changes the label to the respective break times
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
                self.timer.start(20) #starts the next study session
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
            else:
                hours= int(remaining_time//3600)
                minutes = int(remaining_time//60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)
                
            
        
    def get_timer_duration(self):   #This will assign the time period for which the timers will act 
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
    def get_break_timer_duration(self): #same function as above but for break times
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
        
    def simplelevel(self):  #this sets the label to the respective session length and changes the mode text
        self.timer_label.setText("00:00:30")
        self.mode.setText("Simple")

    def mediumlevel(self):
        self.timer_label.setText("02:00:00")
        self.mode.setText("Medium")

    def intenselevel(self):
        self.timer_label.setText("03:00:00")
        self.mode.setText("Intense")
        
    def setup_animations(self):      #creates a slow opening of the app
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()     
        
    def reset_timer(self):      #resets the timer to their respective times , it wont reset the time for break
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
        
    def pause_resume_timer(self):  #pause resume timer function for the study session
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
                    
    def break_pause_resume_timer(self): #pause resume timer function for breaks
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
                
    def minimize_to_system_tray(self): #function for allowing the app to minimize to system tray
        self.hide()
        if not hasattr(self, 'tray_icon'):
            self.create_system_tray_icon()

    def create_system_tray_icon(self): #for creating system tray icon
        menu = QMenu(self)
        open_action = menu.addAction("Open")  #adds the capability to open and exit the app in the system tray
        open_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/logo.jpg")) #sets logo when in system tray
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def close_application(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        sys.exit()

    def play_sound(self, sound_effect): #function for playing the notify sound
        if sound_effect.isLoaded():
            sound_effect.play()
        else:
            print("Error: Sound file not loaded.")


if __name__ == "__main__":
    app = QApplication(sys.argv)           #parameter allows command-line arguments to be passed to the application.
    window = MyMainWindow()                #creates a mainwindow class which is represents the main window
    window.show()                          #makes main window visible
    sys.exit(app.exec_())                  #ensures clean exit of the program
