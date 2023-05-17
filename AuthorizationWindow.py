import sys

import pyodbc
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password
from MainWindowAdmin import MainWindowAdmin
from MainWindowStudent import MainWindowStudent
from MainWindowTeacher import MainWindowTeacher


class AuthorizationWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Interface/authorization.ui', self)
        self.setWindowTitle('Авторизация')
        self.start_btn.clicked.connect(self.start)
        self.user = 'учитель'
        self.mode.activated[str].connect(self.change_user)

    def change_user(self, text):
        self.user = text

    def start(self):
        password = str(self.password_LineEdit.text())
        id = str(self.id_LineEdit.text())
        if id not in teacher_password.keys() and self.user == 'учитель':
            self.wrong_pass.setText('Неверный id')
        elif id not in student_password.keys() and self.user == 'ученик/родитель':
            self.wrong_pass.setText('Неверный id')
        elif self.user == 'учитель' and password == teacher_password[id]:
            self.mainwindow = MainWindowTeacher(id)
            self.mainwindow.show()
            self.close()
        elif self.user == 'ученик/родитель' and password == student_password[id]:
            self.mainwindow = MainWindowStudent(id)
            self.mainwindow.show()
            self.close()
        elif self.user == 'admin' and password == admin_password:
            self.mainwindow = MainWindowAdmin()
            self.mainwindow.show()
            self.close()
        else:
            self.wrong_pass.setText('Неверный пароль')
