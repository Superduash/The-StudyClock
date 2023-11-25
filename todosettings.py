import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from plyer import notification
import sqlite3

class todoSettings(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('todosettings.ui', self)