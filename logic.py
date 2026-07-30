import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from gui import Ui_MainWindow


class Attendee:

    def __init__(self, name: str, email: str, phone: str, ticket: str) -> None:
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__ticket = ticket

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email

    def get_phone(self) -> str:
        return self.__phone

    def get_ticket(self) -> str:
        return self.__ticket

    def to_csv_row(self) -> list[str]:
        return [self.__name, self.__email, self.__phone, self.__ticket, "N/A"]


class VIPAttendee(Attendee):

    def __init__(self, name: str, email: str, phone: str, ticket: str, vip_code: str) -> None:
        super().__init__(name, email, phone, ticket)
        self.__vip_code = vip_code

    def get_vip_code(self) -> str:
        return self.__vip_code

    def to_csv_row(self) -> list[str]:
        return [
            self.get_name(),
            self.get_email(),
            self.get_phone(),
            self.get_ticket(),
            f"VIP (Code: {self.__vip_code})"
        ]

class Speaker(Attendee):

    def __init__(self, name: str, email: str, phone: str, ticket: str, speaker_code: str) -> None:
        super().__init__(name, email, phone, ticket)
        self.__speaker_code = speaker_code

    def get_topic(self) -> str:
        return self.__speaker_code

    def to_csv_row(self) -> list[str]:
        return [
            self.get_name(),
            self.get_email(),
            self.get_phone(),
            self.get_ticket(),
            f"Speaker (Code: {self.__speaker_code})"
            ]
        


class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) #Makes sure the welcome page is visible first
        self.input_vip.setEnabled(False) #Disables the VIP input box (grays out)
        self.button_start.clicked.connect(self.page_switch)
        self.combo_ticket.currentIndexChanged.connect(self.code)
        self.button_submit.clicked.connect(self.submit)
        self.code()

    def page_switch(self):
        self.stackedWidget.setCurrentIndex(1)


    def code(self) -> None:
        selected_ticket = self.combo_ticket.currentText()
        if selected_ticket == "VIP":
            self.label_code.setText("Enter VIP Code")
            self.label_code.setVisible(True)
            self.input_code.setVisible(True)
        elif selected_ticket == "Speaker":
            self.label_code.setText("Enter Speaker Code")
            self.label_code.setVisible(True)
            self.input_code.setVisible(True)
        else:
           self.label_code.setVisible(False)
           self.input_code.setVisible(False)
           self.input_code.clear() 


    def submit(self) -> None:
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        phone = self.input_phone.text().strip()
        code = self.input_code.text().strip()
        ticket = self.combo_ticket.currentText()

        if not name or not email or not phone:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("All fields are required!")
            return

        if not name.replace(" ", "").isalpha():
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Name must contain letters only.")
            return

        if "@" not in email or "." not in email:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Please enter a valid email address.")
            return

        if not phone.isdigit():
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Phone number must contain digits only!")
            return
        
        if ticket == "Select your ticket":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Must select a ticket!")
            return

        if ticket == "VIP" and code != "VIP2026":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Invalid VIP Passcode!")
            return

        if ticket == "Speaker" and code != "SPEAKER2026":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Invalid Speaker Passcode!")

        if self.saved_phones(phone):
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Guest with this phone number is already registered!")
            return

        if ticket == "VIP":
            attendee = VIPAttendee(name, email, phone, ticket, code)
        elif ticket == "Speaker":
            attendee = Speaker(name, email, phone, ticket, code)
        else:
            attendee = Attendee(name, email, phone, ticket)

        try:
            with open("records.csv", mode = "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(attendee.to_csv_row)

            self.label_status.setStyleSheet("color: green")
            self.label_status.setText("Registration Successful!")

            self.input_name.clear()
            self.input_email.clear()
            self.input_phone.clear()
            self.input_vip.clear()
            self.combo_ticket.setCurrentIndex(0)
        except Exception:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Error: Could not save registration")


    def saved_phones(self, phone: str) -> bool:
        try:
            with open("records.csv", mode = "r", newline = "") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 2 and row[2] == phone:
                        return True
        except FileNotFoundError:
            return False
        return False



             
