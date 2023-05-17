import pyodbc
import pandas as pd

'''
cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=DESKTOP-5MRJL6K\SQLEXPRESS;"
                      "Database=SchoolDB;"
                      "Trusted_Connection=yes;")

print(f"EXEC GetClassSchedule @classPar = {11},  @classLit = '{1}', "
      f"@HalfYID = {5} \nGO")

cursor = cnxn.cursor()

cursor.execute(f'select cl.parallel, cl.litera from Classes cl inner join Teacher_Class tc on cl.ID = tc.Class_ID '
                       f'inner join Teachers th on tc.Teacher_ID = th.ID where th.id = {1}')

print(cursor.rowcount)


rowcount = cursor.fetchall()[0][0]
print(rowcount)

cursor.execute(f"EXEC GetClassSchedule @classPar = {11},  @classLit = '{1}', "
               f"@HalfYID = {5}")
for row in cursor:
    print(row)

'''
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QMainWindow, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [
            [4, 9, 2],
            [1, "hello", 0],
            [3, 5, 0],
            [3, 3, "what"],
            ["this", 8, 9],
        ]

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)

        self.table.setModel(self.proxy_model)

        self.searchbar = QLineEdit()

        # You can choose the type of search by connecting to a different slot here.
        # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

        layout = QVBoxLayout()

        layout.addWidget(self.searchbar)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
'''\
'''
cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=DESKTOP-5MRJL6K\SQLEXPRESS;"
                      "Database=SchoolDB;"
                      "Trusted_Connection=yes;")

cursor = cnxn.cursor()


for row in cursor:
    data.append(row)
    for i in range(self.cols):
        if i == 0:
            item = QTableWidgetItem(days[row[i]])
        else:
            item = QTableWidgetItem(str(row[i]))
        self.tableWidget.setItem(k, i, item)
    k += 1
self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
self.tableWidget.resizeColumnsToContents()

self.proxy_model = QSortFilterProxyModel()
self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
self.proxy_model.setSourceModel(self.tableWidget)

self.proxy_model.sort(0, Qt.AscendingOrder)

self.tableWidget.setModel(self.proxy_model)

self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

for row in self.cursor:
        data.append(row)
        for i in range(self.cols):
            if i == 0:
                item = QTableWidgetItem(days[row[i]])
            else:
                item = QTableWidgetItem(str(row[i]))
            self.tableWidget.setItem(k, i, item)
        k += 1
        
    self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    self.tableWidget.resizeColumnsToContents()
    
        
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.cols)
        self.tableWidget.setHorizontalHeaderLabels(["День недели", "Смена", 'Номер урока', "Предмет", "Кабинет", "Учитель"])
        
'''

'''self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.cols)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Дата", "Предмет", 'Оценка'])
        self.cursor.execute(self.q)
        k = 0
        for row in self.cursor:
            for i in range(self.cols):
                item = QTableWidgetItem(str(row[i]))
                self.tableWidget.setItem(k, i, item)
            print(row)
            k += 1
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.resizeColumnsToContents()'''


cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=DESKTOP-5MRJL6K\SQLEXPRESS;"
                      "Database=SchoolDB;"
                      "Trusted_Connection=yes;")

sql_select_Query = "select * from Students"
# MySQLCursorDict creates a cursor that returns rows as dictionaries
cursor = cnxn.cursor()
cursor.execute(sql_select_Query)
columns = [column[0] for column in cursor.description]
print(columns)

records = cursor.fetchall()
