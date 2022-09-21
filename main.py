import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt

from gui.slideShow import SlideShow


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        s = SlideShow()
        s.setInterval(1000)
        s.setFixedWidth(300)
        s.setFixedHeight(900)
        s.setFilenames(["./images/default_01.jpg", "./images/default_02.jpg", "./images/default_03.jpg"])

        grid.addWidget(s, 0, 0)


        self.setWindowTitle('Smart Kiosk')
        self.resize(300,900)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())


