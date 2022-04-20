import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow


def display():
    print(line_edit.text())


def quit_window():
    window.close()


app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(500, 500, 300, 300)
window.setWindowTitle("FirstQt")

label = QLabel(window)
label.setText("PyQt5 GUI Application")
label.adjustSize()
label.move(90, 30)

line_edit = QLineEdit(window)
line_edit.move(100, 70)

button = QPushButton(window)
button.setText("Print")
button.clicked.connect(display)
button.move(100, 130)

button2 = QPushButton(window)
button2.setText("Quit")
button2.clicked.connect(quit_window)
button2.move(100, 170)

window.show()
sys.exit(app.exec_())
