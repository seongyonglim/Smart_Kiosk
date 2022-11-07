import threading
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt

from gui.MenuMnView_v2 import *
from gui.slideShow import SlideShow
from gui.MenuView import *
from util.detect_age import Detector


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


def startAd():
    pass
    # t = threading.Thread(target=sum, args=(1, 100000))
    # t.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()
    # sys.exit()
    app = None
    while 1:
        if app:
            del app
        app = QApplication(sys.argv)
        obj = Detector()
        data = obj.detector()
        age_split = str(data).split('/')[1]
        age = age_split.split("~")[0]
        if(int(age[1:len(age)]) >= 55):
            window = MinMenu()
            window.show()
        else :
            window = Menu()
            window.show()
        app.exec_()



