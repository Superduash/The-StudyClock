import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1100, 600))
        self.widget.setObjectName("widget")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.bg = QtWidgets.QLabel(self.frame)
        self.bg.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("../CS-Project/resources/bg.jpg"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 900, 121))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.title_2 = QtWidgets.QLabel(self.frame_2)
        self.title_2.setGeometry(QtCore.QRect(0, 0, 711, 121))
        self.title_2.setText("")
        self.title_2.setPixmap(QtGui.QPixmap("../CS-Project/resources/finished_assigments.png"))
        self.title_2.setScaledContents(True)
        self.title_2.setObjectName("title_2")
        self.complete_table = QtWidgets.QTableWidget(self.frame)
        self.complete_table.setGeometry(QtCore.QRect(0, 130, 361, 471))
        self.complete_table.setStyleSheet(" background-color: transparent;")
        self.complete_table.setObjectName("complete_table")
        self.complete_table.setColumnCount(2)
        self.complete_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.complete_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.complete_table.setHorizontalHeaderItem(1, item)
        self.complete_table.horizontalHeader().setDefaultSectionSize(180)
        self.done = QtWidgets.QPushButton(self.frame)
        self.done.setGeometry(QtCore.QRect(370, 200, 200, 60))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Semib")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.done.setFont(font)
        self.done.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 2px solid black;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 0, 255, 50);\n"
"    border: 2px solid #000080;\n"
"    transition: background-color 0.3s, border 0.3s; \n"
"}")
        self.done.setObjectName("done")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.complete_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Completed Tasks"))
        item = self.complete_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date of Completition"))
        self.done.setText(_translate("MainWindow", "Done"))
