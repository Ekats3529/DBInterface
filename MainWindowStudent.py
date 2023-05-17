import sys

import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password, cursor
from ShowTableWindow import ShowTableWindow
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel


class MainWindowStudent(QMainWindow):
    def __init__(self, id):
        super().__init__()
        uic.loadUi('Interface/student_main.ui', self)
        self.id = int(id)
        self.setWindowTitle(f'Ученик | id : {self.id}')

        self.surname, self.name, self.secondname, self.parallel, self.litera = self.get_attributes()
        self.set_label_name()
        self.chosen_halfy = None
        self.set_combobox_HY()
        self.comboBox_HY.activated[str].connect(self.halfy)
        self.pushButton_schedule.clicked.connect(self.show_schedule)
        self.pushButton_marks.clicked.connect(self.show_marks)

    def get_attributes(self):
        cursor = cnxn.cursor()

        cursor.execute(f'select st.surname, st.name, st.secondname, cl.parallel, cl.litera from Students st'
                       f' inner join Classes cl on st.Class_ID = cl.ID where st.ID = {self.id}')

        surname, name, secondname, parallel, litera = None, None, None, None, None

        for row in cursor:
            surname = row[0]
            name = row[1]
            secondname = row[2]
            parallel = row[3]
            litera = row[4]

        return surname, name, secondname, parallel, litera

    def set_label_name(self):
        str = f"Ученик: {self.surname} {self.name} {self.secondname}"
        str1 = f" класс {self.parallel}-{self.litera}"
        self.label_name.setText(str + str1)

    def halfy(self, text):
        self.chosen_halfy = text

    def set_combobox_HY(self):
        self.comboBox_HY.clear()
        self.dct_HY = {}
        cursor = cnxn.cursor()

        cursor.execute(f'select id, number, datepart(year, EndDate) from HalfYears')

        for row in cursor:
            if row[1] == 1:
                self.dct_HY[f'{row[1]} полугодие {row[2]}/{row[2] + 1}'] = row[0]
                self.comboBox_HY.addItem(f'{row[1]} полугодие {row[2]}/{row[2] + 1}')
            else:
                self.dct_HY[f'{row[1]} полугодие {row[2] - 1}/{row[2]}'] = row[0]
                self.comboBox_HY.addItem(f'{row[1]} полугодие {row[2] - 1}/{row[2]}')

    def show_schedule(self):

        cursor.execute(f"EXEC GetClassSchedule @classPar = {self.parallel},  @classLit = '{self.litera}', "
                       f"@HalfYID = {self.dct_HY[self.chosen_halfy]}")

        cursor.execute('select @@rowcount')

        rowcount = cursor.fetchall()[0][0]

        if rowcount == 0:
            self.label_nosch.setText("Расписание не найдено")
        else:
            self.label_nosch.setText("")
            q = f"EXEC GetClassSchedule @classPar = {self.parallel},  @classLit = '{self.litera}', @HalfYID = {self.dct_HY[self.chosen_halfy]}"
            show_schedule_window = ShowTableWindow(self, q, f'Расписание класса {self.parallel}-{self.litera}', rowcount, 6)
            show_schedule_window.show()
            show_schedule_window.exec()

    def show_marks(self):
        cursor.execute(f"EXEC GetStudentMarks @StudentId = {self.id}, "
                       f"@HalfYID = {self.dct_HY[self.chosen_halfy]}")

        cursor.execute('select @@rowcount')

        rowcount = cursor.fetchall()[0][0]

        if rowcount == 0:
            self.label_nomk.setText("Оценки не найдены")
        else:
            pass
            self.label_nomk.setText("")
            q = f"EXEC GetStudentMarks @StudentId = {self.id}, @HalfYID = {self.dct_HY[self.chosen_halfy]}"
            show_mk_window = ShowTableWindow(self, q, 'Оценки', rowcount, 3)
            show_mk_window.show()
            show_mk_window.exec()
