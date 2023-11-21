import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import timedelta, datetime
from plyer import notification
from PyQt5.QtMultimedia import QSoundEffect
import mysql.connector
from todolistgui import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        def addit(self):
            task_text = self.task_input.toPlainText()  
            if task_text:
                    item = QListWidgetItem()
                    checkbox_item = QCheckBox(task_text)
                    item.setSizeHint(checkbox_item.sizeHint())
                    self.task_list.addItem(item)
                    self.task_list.setItemWidget(item, checkbox_item)
                    self.task_input.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())