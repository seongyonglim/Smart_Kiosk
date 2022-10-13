import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from util.ReadDataBase import ReadDB
import time

form_class = uic.loadUiType("../resources/menu.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.readDb =  ReadDB()

        ###########################################
        # 오더 위젯들 리스트
        self.order_layout_list = []


        ###########################################

        # 카테고리 다음 이전 버튼
        self.category_index_button = [self.prevButton, self.nextButton]
        # 메뉴 인덱스 다음 이전 버튼
        self.menu_index_button = [self.menu_prev_button, self.menu_next_button]

        # 카테고리 버튼 레이아웃
        self.category_button_layout = self.category_button_layout
        self.category_button_list = []
        # 카테고리 버튼 String
        self.category_name_list = ["추천메뉴", "햄버거", "음료", "사이드"]


        ###########################################
        # 상품
        # 상품 이미지 리스트
        self.image_list = [self.product_image_1,self.product_image_2,self.product_image_3,self.product_image_4,
                           self.product_image_5,self.product_image_6,self.product_image_7,self.product_image_8]
        # 상품 이름 리스트
        self.name_list  = [self.product_name_1, self.product_name_2, self.product_name_3, self.product_name_4,
                           self.product_name_5, self.product_name_6, self.product_name_7, self.product_name_8]
        # 상품 가격 리스트
        self.price_list = [self.product_price_1, self.product_price_2, self.product_price_3, self.product_price_4,
                           self.product_price_5, self.product_price_6, self.product_price_7, self.product_price_8]

        ###########################################
        # 카테고리 버튼 생성
        self.createCategoryButton()
        # 카테고리 1 메뉴 로드
        self.createMenu(1)
        self.addOrder("order_name", 3, 1000)
        self.addOrder("order_name", 1, 2000)

        self.order_layout_list[0][1].setText("HEllo")
        self.order_list_layout.removeItem(0)

    def createCategoryButton(self):
        for cur in range(0,len(self.category_name_list)):
            category_button = QPushButton(self.category_name_list[cur])
            category_button.setFixedSize(QSize(121, 71))
            self.category_button_list.append(category_button)
            self.category_button_layout.addWidget(category_button)

        # 람다식 선언은 직접 선언해야되므로 for문으로 생성불가
        self.category_button_list[0].clicked.connect(lambda: self.createMenu(0))
        self.category_button_list[1].clicked.connect(lambda: self.createMenu(1))
        self.category_button_list[2].clicked.connect(lambda: self.createMenu(2))
        self.category_button_list[3].clicked.connect(lambda: self.createMenu(3))

    def addOrder(self, order_name, count, price):
        order_widgets_list = []
        orderHB = QHBoxLayout()
        orderHB.addStretch(8)

        order_no_label      = QLabel(str(len(self.order_layout_list) + 1))
        order_name_label    = QLabel(order_name)

        order_num_plus_btn = QPushButton("+")
        order_count_label   = QLabel(str(count))
        order_num_minus_btn = QPushButton("-")

        order_price_label   = QLabel(str(price))
        order_price_total   = QLabel(str(count * price))

        order_cancle_btn     = QPushButton("X")

        orderHB.addWidget(order_no_label)
        orderHB.addWidget(order_name_label)

        orderHB.addWidget(order_num_plus_btn)
        orderHB.addWidget(order_count_label)
        orderHB.addWidget(order_num_minus_btn)

        orderHB.addWidget(order_price_label)
        orderHB.addWidget(order_price_total)

        orderHB.addWidget(order_cancle_btn)

        # 리스트에 추가
        order_widgets_list.append(orderHB)
        order_widgets_list.append(order_no_label)
        order_widgets_list.append(order_name_label)

        order_widgets_list.append(order_num_plus_btn)
        order_widgets_list.append(order_count_label)
        order_widgets_list.append(order_num_minus_btn)

        order_widgets_list.append(order_price_label)
        order_widgets_list.append(order_price_total)

        order_widgets_list.append(order_cancle_btn)

        order_num_plus_btn.clicked.connect(lambda: self.order_count_plus(order_widgets_list))
        order_num_minus_btn.clicked.connect(lambda: self.order_count_minus(order_widgets_list))
        order_cancle_btn.clicked.connect(lambda: self.order_delete(order_widgets_list))


        self.order_list_layout.addLayout(orderHB)
        self.order_layout_list.append(order_widgets_list)

    def order_count_plus(self,args):
        order_count_label = args[4]
        order_price_label = args[6]
        order_total_label = args[7]


        text = order_count_label.text()
        text = str(int(text) + 1)
        total = str(int(text) * int(order_price_label.text()))

        order_count_label.setText(text)
        order_total_label.setText(total)

    def order_count_minus(self,args):
        order_count_label = args[4]
        order_price_label = args[6]
        order_total_label = args[7]


        text = order_count_label.text()
        if (int(text) - 1) != 0:
            text = str(int(text) - 1)
            total = str(int(text) * int(order_price_label.text()))

            order_count_label.setText(text)
            order_total_label.setText(total)

    def order_delete(self,args):
        order_no_label = args[1]
        no = str(int(order_no_label.text()) -1)
        print(no)
        #self.order_layout_list[no].remove(0)

    def createMenu(self,category):
        readData = self.readDb.getMenu(category)
        print(readData)
        for index in range(0, len(readData)):
            img_obj = QPixmap(readData[index]['p_img_url'])
            # img_obj.scaledToWidth(284)
            # img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText(readData[index]['p_name'])
            self.name_list[index].setFont(QtGui.QFont("굴림", 15))

            self.price_list[index].setText(str(readData[index]['p_price']))
            self.price_list[index].setFont(QtGui.QFont("굴림", 15))

        for index in range(len(readData) + 1, 9):
            index = index - 1
            img_obj = QPixmap("../resources/etc/default.jpg")
            # img_obj.scaledToWidth(284)
            # img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText("")
            self.name_list[index].setFont(QtGui.QFont("굴림", 15))

            self.price_list[index].setText("")
            self.price_list[index].setFont(QtGui.QFont("굴림", 15))

    def test(self):
        img_obj = QPixmap("../resources/etc/default.jpg")
        self.image_list[1].setPixmap(img_obj)
        self.name_list[1].setText("")
        self.name_list[1].setFont(QtGui.QFont("굴림", 15))

        self.price_list[1].setText("")
        self.price_list[1].setFont(QtGui.QFont("굴림", 15))


    def createMenu2(self):
        category = 2
        readData = self.readDb.getMenu(category)
        print(readData)
        for index in range(0, len(readData)):
            img_obj = QPixmap(readData[index]['p_img_url'])
            # img_obj.scaledToWidth(284)
            # img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText(readData[index]['p_name'])
            self.name_list[index].setFont(QtGui.QFont("굴림", 15))

            self.price_list[index].setText(str(readData[index]['p_price']))
            self.price_list[index].setFont(QtGui.QFont("굴림", 15))

        for index in range(len(readData) + 1, 9):
            index = index - 1
            img_obj = QPixmap("../resources/etc/default.jpg")
            # img_obj.scaledToWidth(284)
            # img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText("")
            self.name_list[index].setFont(QtGui.QFont("굴림", 15))

            self.price_list[index].setText("")
            self.price_list[index].setFont(QtGui.QFont("굴림", 15))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()

    myWindow.show()
    app.exec_()