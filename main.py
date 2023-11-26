import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load UI from main.ui
        self.load_ui()

        # Setup UI elements
        self.setup_ui_elements()

    def load_ui(self):
        from PyQt5 import uic

        # Load the UI file
        uic.loadUi('ui/main.ui', self)

    def setup_ui_elements(self):
        # Connect buttons to functions
        self.credits.clicked.connect(self.show_credits)
        self.music.clicked.connect(self.show_music)
        self.twentytimer.clicked.connect(self.open_twenty_timer)
        self.studyfocus.clicked.connect(self.open_study_focus)
        self.taskbuddy.clicked.connect(self.open_task_buddy)
        self.settings.clicked.connect(self.open_settings)
        self.minimizetray.clicked.connect(self.minimize_to_tray)
        self.forceclose.clicked.connect(self.force_close)

        # Setup tray icon
        self.create_system_tray_icon()

    def show_credits(self):
        # Implement your Credits functionality here
        pass

    def show_music(self):
        # Implement your Music functionality here
        pass

    def open_twenty_timer(self):
        # Implement your 20-20-20 Timer functionality here
        pass

    def open_study_focus(self):
        # Implement your Study Focus functionality here
        pass

    def open_task_buddy(self):
        # Implement your Task Buddy functionality here
        pass

    def open_settings(self):
        # Implement your Settings functionality here
        pass

    def minimize_to_tray(self):
        self.hide()
        self.tray_icon.show()

    def force_close(self):
        # Implement your Force Close functionality here
        pass

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
