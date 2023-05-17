import pyodbc
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QCheckBox, QTableWidget, QTableWidgetItem, \
    QVBoxLayout

from main_connections import cnxn, admin_password, teacher_password, student_password, cursor

from AuthorizationWindow import AuthorizationWindow


def main():
    app = QApplication(sys.argv)
    window = AuthorizationWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
