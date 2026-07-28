import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from gui import Ui_MainWindow


class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) #Makes sure the welcome page is visible first
        self.input_vip.setEnabled(False) #Disables the VIP input box (grays out)
        self.button_start.clicked.connect(self.func_one)
        self.combo_ticket.clicked.connect(self.func_two)
        self.button_submit.clicked.connect(self.func_three)





    def vip_select():
