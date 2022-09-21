from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QButtonGroup
from pyqt_ani_radiobutton import AniRadioButton
from pyqt_single_image_graphics_view import SingleImageGraphicsView
from pyqt_svg_button import SvgButton


class SlideShow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__btn = []
        self.__filenames = []



    def __initUi(self):
        self.__view = SingleImageGraphicsView()
        self.__view.setAspectRatioMode(Qt.KeepAspectRatioByExpanding)
        self.__view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__view.setStyleSheet('QGraphicsView { background: transparent; border: none; }')
        self.__view.installEventFilter(self)

        self.__btnGroup = QButtonGroup()
        self.__btnGroup.buttonClicked.connect(self.__showImageOfIdx)

        self.__btnWidget = QWidget()

        self.__prevBtn = SvgButton(self)
        self.__prevBtn.setIcon('./ico/arrow-previous-left-icon.svg')
        self.__prevBtn.setFixedSize(30, 50)
        self.__prevBtn.clicked.connect(self.__prev)
        self.__prevBtn.setEnabled(False)

        self.__nextBtn = SvgButton(self)
        self.__nextBtn.setIcon('./ico/arrow-next-right-icon.svg')
        self.__nextBtn.setFixedSize(30, 50)
        self.__nextBtn.clicked.connect(self.__next)

        lay = QHBoxLayout()
        lay.addWidget(self.__prevBtn, alignment=Qt.AlignLeft)
        lay.addWidget(self.__nextBtn, alignment=Qt.AlignRight)

        self.__navWidget = QWidget()
        self.__navWidget.setLayout(lay)

        lay = QGridLayout()
        lay.addWidget(self.__view, 0, 0, 3, 1)
        lay.addWidget(self.__navWidget, 0, 0, 3, 1)
        lay.addWidget(self.__btnWidget, 2, 0, 1, 1, Qt.AlignCenter)
        self.setLayout(lay)

        self.__timer = QTimer(self)
        self.__timer.setInterval(5000)
        self.__timer.timeout.connect(self.__nextByTimer)
        self.__timer.start()

    def __showImageOfIdx(self, btn):
        idx = self.__btnGroup.id(btn)
        self.__view.setFilename(self.__filenames[idx])
        self.__prevNextBtnToggled(idx)
        self.__timer.start()

    def __prev(self):
        idx = max(0, self.__btnGroup.checkedId()-1)
        self.__btnGroup.button(idx).setChecked(True)
        self.__view.setFilename(self.__filenames[idx])
        self.__prevNextBtnToggled(idx)
        self.__timer.start()

    def __nextByTimer(self):
        idx = (self.__btnGroup.checkedId()+1) % len(self.__btnGroup.buttons())
        self.__btnGroup.button(idx).setChecked(True)
        self.__view.setFilename(self.__filenames[idx])
        self.__prevNextBtnToggled(idx)

    def __next(self):
        idx = min(self.__btnGroup.checkedId()+1, len(self.__btnGroup.buttons())-1)
        self.__btnGroup.button(idx).setChecked(True)
        self.__view.setFilename(self.__filenames[idx])
        self.__prevNextBtnToggled(idx)
        self.__timer.start()

    def __prevNextBtnToggled(self, idx):
        self.__prevBtn.setEnabled(idx != 0)
        self.__nextBtn.setEnabled(idx != len(self.__btnGroup.buttons())-1)



    def mousePressEvent(self, e):
        print('버튼 PRESS')


    def setInterval(self, milliseconds: int):
        self.__timer.setInterval(milliseconds)

    def setFilenames(self, filenames: list):
        self.__filenames = filenames
        lay = QHBoxLayout()
        for i in range(len(self.__filenames)):

            btn = AniRadioButton()
            btn.setFixedSize(30, 15)
            lay.addWidget(btn)
            self.__btn.append(btn)
            self.__btnGroup.addButton(btn, i)
        self.__btn[0].setChecked(True)
        print(self.__filenames)
        self.__view.setFilename(self.__filenames[0])
        self.__btnWidget.setLayout(lay)

    def setNavigationButtonVisible(self, f: bool):
        self.__navWidget.setVisible(f)

    def setBottomButtonVisible(self, f: bool):
        self.__btnWidget.setVisible(f)

    def setTimerEnabled(self, f: bool):
        if f:
            self.__timer.start()
        else:
            self.__timer.stop()