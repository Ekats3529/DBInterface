import sys
import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

import MainWindowStudent, MainWindowTeacher, main_connections, AuthorizationWindow

from ShowTableWindow import ShowTableWindow, TableModel

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password, cursor, days
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
import pandas as pd


tbls = {'Ученики': 'Students', 'Учителя': 'Teachers',
        'Классы': 'Classes', 'Кабинеты': 'Classrooms',
        'Уроки': 'Lessons', 'Оценки': 'Marks',
        'Смены': 'Shifts', 'Полугодия': 'HalfYears',
        'Предметы': 'Subjects', 'Классное руководство': 'Teacher_Class',
        'Соответствие учителя предметам': 'Teacher_Subject',
        'Ответственность за кабинеты': 'Teacher_Classroom'}

class TableModelChange(QAbstractTableModel):

    def __init__(self, data, chosen_table):
        super(TableModelChange, self).__init__()
        self.tasks = [[[str(data[x][i]) if x != " " else " ", False] for x in list(data)] for i in range(data.shape[0])]
        self.labels = list(data)
        self._data = data
        self.chosen_table = chosen_table

    def data(self, index, role):
        if index.isValid():
            data, changed = self.tasks[index.row()][index.column()]
            if role in [Qt.DisplayRole, Qt.EditRole]:
                return data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

    def setData(self, index, value, role):  # !!!
        if role == Qt.EditRole and value.isalpha():
            self.tasks[index.row()][index.column()] = [value, True]
            if self.chosen_table == "Classrooms":
                cursor.execute(f"Update {tbls[self.chosen_table]} set {self.labels[index.column()]} = '{value}' where "
                               f"Number = {self._data['Number'][index.row()]}")
                cnxn.commit()
            else:
                cursor.execute(
                    f"Update {tbls[self.chosen_table]} set {self.labels[index.column()]} = '{value}' where id = {self._data['ID'][index.row()]}")
                cnxn.commit()

            return True
        return False

    def flags(self, index):  # !!!
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class MainWindowAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Interface/admin_main.ui', self)
        self.setWindowTitle('Admin')
        self.chosen_table = 'Ученики'
        self.set_comboBox_tables()
        self.comboBox.activated[str].connect(self.table)
        self.pushButton_shc.clicked.connect(self.show_schedule)

    def table(self, text):
        self.chosen_table = text
        self.show_table()

    def show_schedule(self):

        cursor = cnxn.cursor()
        cursor.execute(f"select * from schedule")
        columns = [column[0] for column in cursor.description]
        k = 0
        for _ in cursor:
            k += 1

        show_schedule_window = ShowTableWindow(self, f"select * from schedule", f'Расписание', k, len(columns))
        show_schedule_window.show()
        show_schedule_window.exec()

    def set_comboBox_tables(self):
        try:
            self.comboBox.clear()
        except Exception as e:
            print(e)
        for tb in tbls.keys():
            self.comboBox.addItem(tb)

    def show_table(self):
        cursor = cnxn.cursor()
        cursor.execute(f"select * from {tbls[self.chosen_table]}")
        columns = [column[0] for column in cursor.description]
        k = 0
        data = []
        for row in cursor:
            data.append([row[i] for i in range(len(row))])
            k += 1
        data = pd.DataFrame(data, columns=columns,
                            index=[str(i) for i in range(1, k + 1)])

        self.model = TableModelChange(data, self.chosen_table)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()
