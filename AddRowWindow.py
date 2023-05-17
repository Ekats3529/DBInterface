import sys

import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password
from MainWindowStudent import MainWindowStudent
from MainWindowTeacher import MainWindowTeacher


from main_connections import cnxn, admin_password, teacher_password, student_password, cursor, days

tbls = {'Ученики': 'Students', 'Учителя': 'Teachers',
        'Классы': 'Classes', 'Кабинеты': 'Classrooms',
        'Уроки': 'Lessons', 'Оценки': 'Marks',
        'Смены': 'Shifts', 'Полугодия': 'HalfYears',
        'Предметы': 'Subjects', 'Классное руководство': 'Teacher_Class',
        'Соответствие учителя предметам': 'Teacher_Subject',
        'Ответственность за кабинеты': 'Teacher_Classroom'}


class AddRowWindow(QDialog):
    def __init__(self, chosen_table):
        super().__init__()
        uic.loadUi('Interface/AddRow.ui', self)
        self.setWindowTitle('AddRowWindow')
        self.pushButton.clicked.connect(self.ok)
        self.chosen_table = chosen_table

    def ok(self):
        row = str(self.lineEdit.text())
        items = row.split()
        q = f"INSERT INTO {tbls[self.chosen_table]} (surname, name, secondname, class_id) VALUES ('{items[0]}', '{items[1]}', '{items[2]}', {items[-1]});"
        cursor.execute(q)
        cnxn.commit()
        self.close()


class DeleteRowWindow(QDialog):
    def __init__(self, chosen_table):
        super().__init__()
        uic.loadUi('Interface/DeleteRowWindow.ui', self)
        self.setWindowTitle('DeleteRowWindow')
        self.pushButton.clicked.connect(self.ok)
        self.chosen_table = chosen_table

    def ok(self):
        row = str(self.lineEdit.text())
        items = row.split()
        q = f"Delete from {tbls[self.chosen_table]} where id = {items[0]}"
        cursor.execute(q)
        cnxn.commit()
        self.close()

