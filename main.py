import sys
import subprocess
import psutil
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.setup_ui_elements()
        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setSource(QUrl.fromLocalFile("resources/click.wav"))

    def load_ui(self):
        from PyQt5 import uic
        uic.loadUi('ui/main.ui', self)

    def setup_ui_elements(self):
        self.credits.clicked.connect(self.show_credits)
        self.music.clicked.connect(self.show_music)
        self.twentytimer.clicked.connect(self.open_twenty_timer)
        self.studyfocus.clicked.connect(self.open_study_focus)
        self.taskbuddy.clicked.connect(self.open_task_buddy)
        self.settings.clicked.connect(self.open_settings)
        self.minimizetray.clicked.connect(self.minimize_to_tray)
        self.forceclose.clicked.connect(self.force_close_all)
        self.create_system_tray_icon()

    def play_click_sound(self):
        self.sound_effect.play()

    def show_credits(self):
        self.play_click_sound()
        # Implement your Credits functionality here

    def show_music(self):
        self.play_click_sound()
        # Implement your Music functionality here

    def open_twenty_timer(self):
        self.play_click_sound()
        subprocess_thread = threading.Thread(target=self.run_subprocess, args=(["python", "202020.py"],))
        subprocess_thread.start()

    def run_subprocess(self, command):
        subprocess.run(command)

    def open_study_focus(self):
        self.play_click_sound()
        # Implement your Study Focus functionality here

    def open_task_buddy(self):
        self.play_click_sound()
        # Implement your Task Buddy functionality here

    def open_settings(self):
        self.play_click_sound()
        # Implement your Settings functionality here

    def minimize_to_tray(self):
        self.play_click_sound()
        self.hide()
        self.tray_icon.show()

    def force_close_all(self):
        self.play_click_sound()
        for proc in psutil.process_iter(['pid', 'name']):
            if "python" in proc.info['name']:
                try:
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    process.wait(timeout=2)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

        sys.exit()


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

    def closeEvent(self, event: QCloseEvent):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
