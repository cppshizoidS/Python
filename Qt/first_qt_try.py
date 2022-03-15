import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow

def dispaly():
    print(line_edit.text())

def quit_window():
    window.close()

app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(500, 500, 300, 300)
window.setWindowTitle("ABOBUS")

label = QLabel(window)
label.setText("PYQt 5 GUI Application")
label.adjustSize()
label.move(90,30)

line_edit =QLineEdit(window)
line_edit.move(100,70)

button = QPushButton(window)
button.setText("Print")
button.clicked.connect(dispaly)
button.move(100,130)

button = QPushButton(window)
button.setText("Quit")
button.clicked.connect(quit_window())
button.move(100,170)

window.show()
sys.exit(app.exec())
