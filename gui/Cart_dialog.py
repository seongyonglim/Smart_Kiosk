import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("../resources/cart_dialog.ui")[0]

class CartDialog(QDialog, form_class):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)


    def showModal(self):
        return super().exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = CartDialog()
    myApp.show()
    app.exec_()