import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime, timedelta
from PyQt5.QtMultimedia import QSoundEffect
from plyer import notification

class OutlinedLabel(QLabel):
    def __init__(self, parent=None):
        super(OutlinedLabel, self).__init__(parent)
        self.text_color = QColor(255, 255, 255)
        self.outline_color = QColor(0, 0, 0)
        self.outline_size = 10

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        pen = QPen(QColor(self.outline_color))
        pen.setWidth(self.outline_size)
        painter.setPen(pen)

        for i in range(-self.outline_size, self.outline_size + 1):
            for j in range(-self.outline_size, self.outline_size + 1):
                if i**2 + j**2 <= self.outline_size**2:
                    painter.drawText(event.rect().adjusted(i, j, 0, 0), self.alignment(), self.text())

        painter.setPen(QColor(self.text_color))
        painter.drawText(event.rect(), self.alignment(), self.text())



class Todo(QMainWindow):
    def __init__(self):
        super().__init__()

        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        initial_width = screen_rect.width() * 1
        initial_height = screen_rect.height() * 0.966

        self.setGeometry(int((screen_rect.width() - initial_width) / 2), int((screen_rect.height() - initial_height) / 2), int(initial_width), int(initial_height))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())

        self.setWindowTitle("ToDo List")

        icon_path = "resources/20-20-20.jpg"
        self.setWindowIcon(QIcon(icon_path))

        self.title = QLabel(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    to_do = Todo()
    to_do.show()
    sys.exit(app.exec_())
