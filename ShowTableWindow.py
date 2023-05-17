import sys

import pyodbc
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password, cursor, days
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
import pandas as pd


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])


class TableModelChange(QAbstractTableModel):

    def __init__(self, data):
        super(TableModelChange, self).__init__()
        self.tasks = [[[str(data[x][i]) if x != " " else " ", False] for x in list(data)] for i in range(data.shape[0])]
        self.labels = list(data)
        self._data = data

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
        if role == Qt.EditRole and index.column() == 6:
            if 1 <= int(value) <= 5:
                self.tasks[index.row()][index.column()] = [value, True]
                cursor.execute(f'Update marks set Mark = {int(value)} where id = {self._data[" "][index.row()]}')
                cnxn.commit()
                return True
        return False

    def flags(self, index):  # !!!
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class ShowTableWindow(QDialog):
    def __init__(self, mainwindow, q, title, rows, cols):
        super().__init__()
        uic.loadUi('Interface/show_schedule.ui', self)
        self.setWindowTitle(title)
        self.mainwindow = mainwindow
        self.cursor = cnxn.cursor()
        self.q = q
        self.rows = rows
        self.cols = cols
        if 'Расписание класса' in title:
            self.show_schedule_class()
        elif title == 'Расписание учителя':
            self.show_schedule_teacher()
        elif title == 'Журнал':
            self.set_marks()
        elif title == "Расписание":
            self.show_schedule()
        else:
            self.show_marks()

    def show_schedule_class(self):
        self.cursor.execute(self.q)
        k = 0
        data = []
        for row in self.cursor:
            data.append([days[row[i]] if i == 0 else row[i] for i in range(len(row))])

        data = pd.DataFrame(data, columns = ["День недели", "Смена", 'Номер урока', "Предмет", "Кабинет", "Учитель"],
                            index=[str(i) for i in range(1, self.rows + 1)])

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()

    def show_schedule_teacher(self):
        self.cursor.execute(self.q)
        k = 0
        data = []
        for row in self.cursor:
            data.append([days[row[i]] if i == 0 else row[i] for i in range(len(row))])

        data = pd.DataFrame(data, columns = ["День недели", "Смена", 'Номер урока', "Предмет", "Кабинет", "Класс"],
                            index=[str(i) for i in range(1, self.rows + 1)])

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()

    def show_marks(self):
        self.cursor.execute(self.q)
        data = []
        for row in self.cursor:
            data.append([row[i] for i in range(len(row))])

        data = pd.DataFrame(data, columns=["Дата", "Предмет", 'Оценка'],
                            index=[str(i) for i in range(1, self.rows + 1)])

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()

    def set_marks(self):
        self.cursor.execute(self.q)
        data = []
        for row in self.cursor:
            data.append([row[i] for i in range(len(row))])

        data = pd.DataFrame(data, columns=[" ", "Дата", "Предмет", 'Класс', 'Фамилия', 'Имя', 'Оценка'],
                            index=[str(i) for i in range(1, self.rows + 1)])

        self.model = TableModelChange(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()

    def show_schedule(self):
        self.cursor.execute(self.q)
        columns = [column[0] for column in self.cursor.description]
        data = []
        for row in self.cursor:
            data.append([row[i] for i in range(len(row))])
        data = pd.DataFrame(data, columns=columns,
                            index=[str(i) for i in range(1, self.rows + 1)])
        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.tableView.setModel(self.proxy_model)
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.tableView.resizeColumnsToContents()




