import csv
from PyQt6.QtWidgets import QMainWindow, QApplication
from gui import Ui_MainWindow


class Attendee:

    '''Class representing an attendee with a standard ticket'''

    def __init__(self, name: str, email: str, phone: str, ticket: str) -> None:
        '''Initializes important attendee details using private attributes'''

        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__ticket = ticket

    def get_name(self) -> str:
        '''Getter for attendee name'''
        return self.__name

    def get_email(self) -> str:
        '''Getter for attendee email'''
        return self.__email

    def get_phone(self) -> str:
        '''Getter for attendee phone number'''
        return self.__phone

    def get_ticket(self) -> str:
        '''Getter for attendee ticket type'''
        return self.__ticket

    def to_csv_row(self) -> list[str]:
        '''Formats attendee details into a list for CSV writing.
        Returns list[str]: formatted attendee data
        '''
        return [self.__name, self.__email, self.__phone, self.__ticket, "N/A"]


class VIPAttendee(Attendee):

    '''Class representing an attendee with a VIP ticket and a passcode'''

    def __init__(self, name: str, email: str, phone: str, ticket: str, vip_code: str) -> None:
        '''Initializes VIP guest details using superclass init and VIP passcode'''

        super().__init__(name, email, phone, ticket)
        self.__vip_code = vip_code

    def get_vip_code(self) -> str:
        '''Getter for VIP passcode'''
        return self.__vip_code

    def to_csv_row(self) -> list[str]:
        '''Overrides parent method to include formatted VIP passcode details
        Returns list[str]: formatted attendee data with VIP passcode
        '''
        return [
            self.get_name(),
            self.get_email(),
            self.get_phone(),
            self.get_ticket(),
            f"VIP (Code: {self.__vip_code})"
        ]

class Speaker(Attendee):

    '''Subclass representing an event speaker with passcode privileges'''

    def __init__(self, name: str, email: str, phone: str, ticket: str, speaker_code: str) -> None:
        '''Initializes Speaker details using superclass init and Speaker passcode'''

        super().__init__(name, email, phone, ticket)
        self.__speaker_code = speaker_code

    def get_speaker_code(self) -> str:
        '''Getter for Speaker passcode'''
        return self.__speaker_code

    def to_csv_row(self) -> list[str]:
        '''Overrides parent method to include formatted Speaker passcode details
        Returns list[str]: formatted attendee data with Speaker passcode
        '''
        return [
            self.get_name(),
            self.get_email(),
            self.get_phone(),
            self.get_ticket(),
            f"Speaker (Code: {self.__speaker_code})"
            ]
        


class Logic(QMainWindow, Ui_MainWindow):
    '''Main window logic controller handling UI signals, validation, and storage'''

    def __init__(self) -> None:
        '''Initializes the main application window, dimensions, and signal connections'''

        super().__init__()
        self.setupUi(self)

        # Makes sure the welcome page is the default page (visible first)
        self.stackedWidget.setCurrentIndex(0) 

        # Connect navigation and submission button signals
        self.button_start.clicked.connect(self.page_switch)
        self.combo_ticket.currentIndexChanged.connect(self.code)
        self.button_submit.clicked.connect(self.submit)

        # Auto-scrolls text inputs to index 0 when the user clicks out of the input
        self.input_name.editingFinished.connect(lambda: self.input_name.setCursorPosition(0))
        self.input_email.editingFinished.connect(lambda: self.input_email.setCursorPosition(0))
        self.input_phone.editingFinished.connect(lambda: self.input_phone.setCursorPosition(0))
        self.input_code.editingFinished.connect(lambda: self.input_code.setCursorPosition(0))

        # Set initial visibility of passcode field based on default ticket state
        self.code()

    def page_switch(self) -> None:
        '''Switch user view from the welcome page to registration form page'''
        self.stackedWidget.setCurrentIndex(1)


    def code(self) -> None:
        '''Toggles passcode label and input field based on selected ticket'''

        selected_ticket = self.combo_ticket.currentText()

        # Shows label and input box respective to VIP tickets
        if selected_ticket == "VIP":
            self.label_code.setText("Enter VIP Code")
            self.label_code.setVisible(True)
            self.input_code.setVisible(True)

        # Shows label and input box respective to Speaker tickets
        elif selected_ticket == "Speaker":
            self.label_code.setText("Enter Speaker Code")
            self.label_code.setVisible(True)
            self.input_code.setVisible(True)

        # Label and input box do not show when Standard ticket is selected
        else:
           self.label_code.setVisible(False)
           self.input_code.setVisible(False)
           self.input_code.clear() 


    def submit(self) -> None:
        '''Validates user input, instantiates attendee objects, and saves records to a csv file'''

        # Retrieves and cleans up inputs
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        # Strips away whitespace and common phone formatting characters (dashes, spaces, parentheses)
        phone = self.input_phone.text().strip().replace("-", "").replace(" ", "").replace(")", "")
        code = self.input_code.text().strip()
        ticket = self.combo_ticket.currentText()

        # 1. Validates required text fields
        if not name or not email or not phone:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("All fields are required!")
            return

        # 2. Validates the name inputs so makes sure there are letters and spaces only
        if not name.replace(" ", "").isalpha():
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Name must contain letters only.")
            return

        # 3. Validates email structure
        if "@" not in email or "." not in email:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Please enter a valid email address.")
            return
        
        # 4. Validates phone number input (digits only and length = 10)
        if not phone.isdigit():
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Please enter a valid phone number.")
            return

        if len(phone) != 10:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Please enter a valid phone number.")
            return

        # 5. Validates ticket selection choice
        if ticket == "Select your ticket":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Must select a ticket!")
            return

        # 6. Validates specific ticket passcodes 
        if ticket == "VIP" and code != "VIP2026":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Invalid VIP Passcode!")
            return

        if ticket == "Speaker" and code != "SPEAKER2026":
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Invalid Speaker Passcode!")
            return

        # 7. Check for duplicate phone number entries
        if self.saved_phones(phone):
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Guest with this phone number is already registered!")
            return
        
        # 8. Instantiates appropriate Attendee object based on ticket type 
        if ticket == "VIP":
            attendee = VIPAttendee(name, email, phone, ticket, code)
        elif ticket == "Speaker":
            attendee = Speaker(name, email, phone, ticket, code)
        else:
            attendee = Attendee(name, email, phone, ticket)

        # 9. Appends attendee object details to csv file
        try:
            with open("records.csv", mode = "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(attendee.to_csv_row())

            # Notifies user that registration was successful and clears all inputs
            self.label_status.setStyleSheet("color: green")
            self.label_status.setText("Registration Successful!")

            self.input_name.clear()
            self.input_email.clear()
            self.input_phone.clear()
            self.input_code.clear()
            self.combo_ticket.setCurrentIndex(0)

        except Exception:
            self.label_status.setStyleSheet("color: red")
            self.label_status.setText("Error: Could not save registration")


    def saved_phones(self, phone: str) -> bool:
        '''Checks the csv to verify whether a phone number has already been registered
        Args: phone(str): The phone number to query
        Returns bool: True if phone number exists in records, False otherwise
        '''

        try:
            with open("records.csv", mode = "r", newline = "") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 2 and row[2] == phone:
                        return True
        except FileNotFoundError:
            return False
        return False