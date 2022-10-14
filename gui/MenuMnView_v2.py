import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from util.ReadDataBase import ReadDB
from PyQt5.QtCore import Qt
import time

import copy
from util.util import Util

form_class = uic.loadUiType("../resources/simple_menu2.ui")[0]
form_class2 = uic.loadUiType("../resources/simple_payment.ui")[0]
class MinMenu(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.readDb = ReadDB()
        self.util   = Util()

        self.readData = self.readDb.getAllMenu()
        self.simple_payment = self.Simple_payment(self)
        self.vlayout = self.main_layout
        self.scrollAreaWidgetContents.setLayout(self.main_layout)
        self.hlayout_list = []
        self.product_list = []

        self.image_label_list = []

        self.name_label_list  = []

        self.price_label_list = []

        print(len(self.readData))
        print(self.readData)
        for index in range(0 , len(self.readData)):
            self.addProduct(self.readData[index])

        '''
        for index in range(0, len(readData)):
            img_obj = QPixmap(readData[index]['p_img_url'])
            img_obj.scaledToWidth(284)
            img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText(readData[index]['p_name'])
            self.name_list[index].setFont(QtGui.QFont("궁서", 20))

            self.price_list[index].setText(str(readData[index]['p_price']))
            self.price_list[index].setFont(QtGui.QFont("궁서", 20))
        '''

    def addProduct(self,row_data):
        product_layout = QVBoxLayout()

        image_label = QLabel()
        name_label  = QLabel(row_data['p_name'])
        price_label = QLabel(str(row_data['p_price']))

        image_label.resize(284, 177)
        name_label.resize(284, 177)
        price_label.resize(284, 177)

        img_obj = QPixmap(row_data['p_img_url'])
        image_label.setPixmap(img_obj)


        name_label.setFont(QtGui.QFont("굴림", 30))
        name_label.setAlignment(Qt.AlignCenter)
        price_label.setFont(QtGui.QFont("굴림", 35))
        price_label.setAlignment(Qt.AlignCenter)

        product_layout.addWidget(image_label)
        product_layout.addWidget(name_label)
        product_layout.addWidget(price_label)

        self.image_label_list.append(image_label)
        self.name_label_list.append(name_label)
        self.price_label_list.append(price_label)
        if len(self.hlayout_list) == 0 or (len(self.image_label_list) % 2) == 1:
            hlayout = QHBoxLayout()
            hlayout.addLayout(product_layout)
            self.hlayout_list.append(hlayout)
            self.vlayout.addLayout(hlayout)
        elif (len(self.image_label_list) % 2) == 0:
            print(len(self.hlayout_list))
            self.hlayout_list[(len(self.hlayout_list)-1)].addLayout(product_layout)

        self.util.clickable(image_label).connect(lambda: self.showDialog(row_data))

    def showDialog(self,data):
        self.simple_payment.setProduct(data)
        self.simple_payment.showModal()
        self.simple_payment.timer()

    class Simple_payment(QDialog, form_class2):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            QDialog.__init__(self, outer_instance)
            self.setupUi(self)

            img_obj = QPixmap("../resources/etc/card.jpg")
            self.card_image.setPixmap(img_obj)
        def showModal(self):
            return super().exec_()

        def setProduct(self,row_data):
            self.row_data = row_data

            # 이미지
            img_obj = QPixmap(self.row_data['p_img_url'])
            self.product_image.setPixmap(img_obj)

            # 상품명
            self.product_name.setText(self.row_data['p_name'])
            # 상품 가격
            self.product_price.setText(str(self.row_data['p_price']))

        def timer(self):
            1==1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MinMenu()
    myWindow.show()
    app.exec_()