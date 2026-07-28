import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from gui import Ui_MainWindow


class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) #Makes sure the welcome page is visible first
        self.input_vip.setEnabled(False) #Disables the VIP input box (grays out)
        self.button_start.clicked.connect(self.page_switch)
        self.combo_ticket.currentIndexChanged.connect(self.ticket_select)
        self.button_submit.clicked.connect(self.submit)

    def page_switch(self):
        self.stackedWidget.setCurrentIndex(1)

    def ticket_select(self):
        selected_ticket = self.combo_ticket.currentText()
        if selected_ticket == "VIP":
            self.input_vip.setEnabled(True)
        else:
           self.input_vip.setEnabled(False)
        self.input_vip.clear() 
    