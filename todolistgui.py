import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 483)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 960, 483))
        self.widget.setObjectName("widget")
        self.bg = QtWidgets.QLabel(self.widget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 960, 483))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("../resources/bg.jpg"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 960, 483))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 961, 101))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.title = QtWidgets.QLabel(self.frame_2)
        self.title.setGeometry(QtCore.QRect(270, -10, 461, 111))
        self.title.setText("")
        self.title.setPixmap(QtGui.QPixmap("../resources/taskbuddy.png"))
        self.title.setScaledContents(True)
        self.title.setObjectName("title")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(30, 120, 221, 131))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.Create_task = QtWidgets.QPushButton(self.frame_3)
        self.Create_task.setGeometry(QtCore.QRect(10, 20, 170, 90))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Semib")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Create_task.setFont(font)
        self.Create_task.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 2px solid black;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 0, 255, 50);\n"
"    border: 2px solid #000080;\n"
"    transition: background-color 0.3s, border 0.3s;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/plus symbol.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Create_task.setIcon(icon)
        self.Create_task.setIconSize(QtCore.QSize(110, 60))
        self.Create_task.setObjectName("Create_task")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(700, 100, 241, 141))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.Settings = QtWidgets.QPushButton(self.frame_4)
        self.Settings.setGeometry(QtCore.QRect(10, 70, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Semib")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Settings.setFont(font)
        self.Settings.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 2px solid black;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 0, 255, 50);\n"
"    border: 2px solid #000080;\n"
"    transition: background-color 0.3s, border 0.3s;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../resources/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Settings.setIcon(icon1)
        self.Settings.setIconSize(QtCore.QSize(100, 50))
        self.Settings.setObjectName("Settings")
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setGeometry(QtCore.QRect(250, 130, 451, 351))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.task_list = QtWidgets.QListWidget(self.frame_5)
        self.task_list.setGeometry(QtCore.QRect(0, 60, 401, 271))
        self.task_list.setStyleSheet("\n"
"")
        self.task_list.setObjectName("task_list")
        self.task_list_title = QtWidgets.QLabel(self.frame_5)
        self.task_list_title.setGeometry(QtCore.QRect(0, 0, 381, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small Semibol")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.task_list_title.setFont(font)
        self.task_list_title.setObjectName("task_list_title")
        self.frame_7 = QtWidgets.QFrame(self.frame)
        self.frame_7.setGeometry(QtCore.QRect(700, 260, 211, 51))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.Completed = QtWidgets.QPushButton(self.frame_7)
        self.Completed.setGeometry(QtCore.QRect(10, 0, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Semib")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Completed.setFont(font)
        self.Completed.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: 2px solid black;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 0, 255, 50);\n"
"    border: 2px solid #000080;\n"
"    transition: background-color 0.3s, border 0.3s;\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../resources/todolisticon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Completed.setIcon(icon2)
        self.Completed.setIconSize(QtCore.QSize(141, 51))
        self.Completed.setObjectName("Completed")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setGeometry(QtCore.QRect(30, 250, 201, 211))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.entertask = QtWidgets.QLabel(self.frame_6)
        self.entertask.setGeometry(QtCore.QRect(0, 10, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Semib")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.entertask.setFont(font)
        self.entertask.setObjectName("entertask")
        self.task_input = QtWidgets.QTextEdit(self.frame_6)
        self.task_input.setGeometry(QtCore.QRect(0, 60, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display")
        font.setPointSize(12)
        self.task_input.setFont(font)
        self.task_input.setObjectName("task_input")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def addit(self):
            task_text = self.task_input.toPlainText()  
            if task_text:
                    item = QListWidgetItem()
                    checkbox_item = QCheckBox(task_text)
                    item.setSizeHint(checkbox_item.sizeHint())
                    self.task_list.addItem(item)
                    self.task_list.setItemWidget(item, checkbox_item)
                    self.task_input.clear()    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Create_task.setText(_translate("MainWindow", "Enter"))
        self.Settings.setText(_translate("MainWindow", "Settings"))
        self.task_list_title.setText(_translate("MainWindow", "Today\'s Mission :"))
        self.Completed.setText(_translate("MainWindow", "Completed"))
        self.entertask.setText(_translate("MainWindow", "Enter the task :"))
        self.task_input.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Variable Display\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:7.8pt;\"><br /></p></body></html>"))
