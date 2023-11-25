import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from plyer import notification
import sqlite3

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('finishdassigmentsui.ui', self)