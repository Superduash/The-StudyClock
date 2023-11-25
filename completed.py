import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from plyer import notification
import sqlite3

conn = sqlite3.connect('task_buddy.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists completed_tasks(
    task text
    date_of_completion text
    time_of_completion text
    row_id int   
    )""")
c.execute('DROP TABLE completed_tasks')
conn.commit()
conn.close()

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
    def close_connection(self):
        self.conn.close()
        
    def delete_task(self, row_id):
        self.conn = sqlite3.connect('task_buddy.db')
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM todo_list WHERE row_id = ?", (row_id,))
        self.conn.commit()

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('finishdassigmentsui.ui', self)
        
        self.collectall()
        

        
    def delete_task_2(self):
        pass
    def collectall(self):
        pass