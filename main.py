import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
app = QApplication([])
window = QMainWindow()
window.setWindowTitle("The StudyClock")
cw = QWidget()
window.setCentralWidget(cw)
layout = QVBoxLayout()
layout.addWidget(QLabel("Welcome to The StudyClock!!"))
layout.addWidget(QPushButton("Start Timer"))
layout.addWidget(QPushButton("Settings"))
cw.setLayout(layout)
window.show()

