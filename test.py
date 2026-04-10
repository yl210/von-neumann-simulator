import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        
        self.setWindowTitle('my app')
        self.setFixedSize(QSize(400,300))
        w, h = self.width(), self.height()

        self.button = QPushButton('button!')
        self.button.setFixedSize(QSize(100, 50))
        self.button.clicked.connect(self.buttonClicked)

        self.setCentralWidget(self.button)

    def buttonClicked(self):
        self.button.setText('already clicked')
        self.button.setEnabled(False)

        self.setWindowTitle('my oneshot app')

    '''
    def buttonToggled(self, checked):
        self.button_is_checked = checked
        print('toggled?', checked)
    '''
    
    def buttonReleased(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()