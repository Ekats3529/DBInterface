import sys

import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, QVBoxLayout



admin_password = '12345'
teacher_password = {'1': '123', '5': '11', '2': '1'}
student_password = {'1': '1', '425': '1'}
days = {1: "понедельник",
        2: "вторник",
        3: "среда",
        4: "четверг",
        5: "пятница",
        6: "суббота"}

cnxn = pyodbc.connect("Driver={SQL Server};"
                          "Server=DESKTOP-5MRJL6K\SQLEXPRESS;"
                          "Database=SchoolDB;"
                          "Trusted_Connection=yes;")

cursor = cnxn.cursor()