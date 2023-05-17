import sys

import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password, cursor
from ShowTableWindow import ShowTableWindow
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel


class MainWindowTeacher(QMainWindow):
    def __init__(self, id):
        super().__init__()
        uic.loadUi('Interface/teacher_main.ui', self)
        self.id = int(id)
        self.setWindowTitle(f'Учитель | id : {self.id}')
        self.surname, self.name, self.secondname = self.get_attributes()
        self.set_label_name()
        self.chosen_halfy = None
        self.set_combobox_HY()
        self.set_cl()
        self.set_cab()
        self.comboBox_HY.activated[str].connect(self.halfy)
        self.pushButton_schedule.clicked.connect(self.show_schedule)
        self.pushButton_marks.clicked.connect(self.show_marks)

    def get_attributes(self):
        cursor = cnxn.cursor()

        cursor.execute(f'select st.surname, st.name, st.secondname from Teachers st'
                       f' where st.ID = {self.id}')

        surname, name, secondname = None, None, None

        for row in cursor:
            surname = row[0]
            name = row[1]
            secondname = row[2]

        return surname, name, secondname

    def set_cl(self):
        cursor = cnxn.cursor()

        cursor.execute(f'select cl.parallel, cl.litera from Classes cl inner join Teacher_Class tc on cl.ID = tc.Class_ID '
                       f'inner join Teachers th on tc.Teacher_ID = th.ID where th.id = {self.id}')

        if cursor.rowcount == 0:
            self.label_cl.setText("нет классного руководства")
        else:
            for row in cursor:
                self.label_cl.setText(f"{row[0]}-{row[1]} класс")

    def set_cab(self):
        cursor = cnxn.cursor()

        cursor.execute(
            f'select cl.number from Classrooms cl inner join Teacher_Classroom tc on cl.Number = tc.Classroom_number '
            f'inner join Teachers th on tc.Teacher_ID = th.ID where th.id = {self.id}')

        if cursor.rowcount == 0:
            self.label_cab.setText("нет кабинета")
        else:
            for row in cursor:
                self.label_cab.setText(f"{row[0]} кабинет")


    def set_label_name(self):
        str = f"Учитель: {self.surname} {self.name} {self.secondname}"
        self.label_name.setText(str)

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
        cursor.execute( f"EXEC GetTeacherSchedule @ID = {self.id}, @HalfYID = {self.dct_HY[self.chosen_halfy]}")

        cursor.execute('select @@rowcount')
        rowcount = cursor.fetchall()[0][0]

        if rowcount == 0:
            self.label_nosch.setText("Расписание не найдено")
        else:
            self.label_nosch.setText("")
            q = f"EXEC GetTeacherSchedule @ID = {self.id}, @HalfYID = {self.dct_HY[self.chosen_halfy]}"

            show_schedule_window = ShowTableWindow(self, q, 'Расписание учителя', rowcount, 6)
            show_schedule_window.show()
            show_schedule_window.exec()

    def show_marks(self):
        cursor.execute(f"EXEC GetTeacherMarks @TeacherId = {self.id}, "
                       f"@HalfYID = {self.dct_HY[self.chosen_halfy]}")

        cursor.execute('select @@rowcount')

        rowcount = cursor.fetchall()[0][0]

        if rowcount == 0:
            self.label_nomk.setText("Оценки не найдены")
        else:
            self.label_nomk.setText("")
            q = f"EXEC GetTeacherMarks @TeacherId = {self.id}, @HalfYID = {self.dct_HY[self.chosen_halfy]}"
            show_mk_window = ShowTableWindow(self, q, 'Журнал', rowcount, 6)
            show_mk_window.show()
            show_mk_window.exec()