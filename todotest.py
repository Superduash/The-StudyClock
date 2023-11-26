import sys
from PyQt5.QtWidgets import QApplication
from todolistgui import SettingsDialog

app = QApplication(sys.argv)
dialog = SettingsDialog()
result = dialog.exec_()
print(f"Dialog result: {result}")
