from logic import *

def main() -> None:
    '''Initializes and run the Event Guest Manager GUI application'''
    
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()