import sys

from PyQt5.QtCore import QSize, pyqtSignal, QEvent, QObject
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import copy
from gui.Cart_dialog import CartDialog
from util.ReadDataBase import ReadDB
import time

form_class = uic.loadUiType("../resources/menu.ui")[0]

dialog_form_class = uic.loadUiType("../resources/cart_dialog.ui")[0]


class Menu(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.readDb =  ReadDB()

        # 장바구니 다이얼 로그 생성
        self.cartDialog = self.createDialog()
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

    def createCategoryButton(self):
        for cur in range(0,len(self.category_name_list)):
            category_button = QPushButton(self.category_name_list[cur])
            category_button.setFixedSize(QSize(121, 71))
            self.category_button_list.append(category_button)
            self.category_button_layout.addWidget(category_button)

        self.category_button_list[0].clicked.connect(lambda: self.createMenu(0))
        self.category_button_list[1].clicked.connect(lambda: self.createMenu(1))
        self.category_button_list[2].clicked.connect(lambda: self.createMenu(2))
        self.category_button_list[3].clicked.connect(lambda: self.createMenu(3))

    def addOrder(self, order_name, count, price):
        order_widgets_list = []
        orderHB = QHBoxLayout()
        orderHB.addStretch(8)

        # 주문하기 위젯 생성
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

        # 버튼들 이벤트 추가
        order_num_plus_btn.clicked.connect(lambda: self.order_count_plus(order_widgets_list))
        order_num_minus_btn.clicked.connect(lambda: self.order_count_minus(order_widgets_list))
        order_cancle_btn.clicked.connect(lambda: self.order_delete(order_widgets_list))


        self.order_list_layout.addLayout(orderHB)
        self.order_layout_list.append(order_widgets_list)


        self.order_total_price_cal()

    ##########################################################
    ##########      주문 리스트의 버튼 시작
    ##########################################################
    def order_count_plus(self,args):
        order_count_label = args[4]
        order_price_label = args[6]
        order_total_label = args[7]


        text = order_count_label.text()
        text = str(int(text) + 1)
        total = str(int(text) * int(order_price_label.text()))

        order_count_label.setText(text)
        order_total_label.setText(total)

        self.order_total_price_cal()

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
            self.order_total_price_cal()

    def order_delete(self,args):
        order_no_label = args[1]
        no = int(int(order_no_label.text()) -1)

        self.boxdelete(self.order_layout_list[no][0])
        del self.order_layout_list[no]

        for i in range(0,len(self.order_layout_list)):
            self.order_layout_list[i][1].setText(str(i+1))
        self.order_total_price_cal()
    # 총 금액 계산
    def order_total_price_cal(self):
        total_price = 0
        for i in range(0, len(self.order_layout_list)):
            total_price += int(self.order_layout_list[i][7].text())
        self.total_price_label.setText(str(total_price))

    ##########################################################
    ##########      주문 리스트의 버튼 끝
    ##########################################################

    def showDialog(self,data):
        self.cartDialog.setProduct(data)
        self.cartDialog.showModal()

    def noneMethod(self):
        1==1
    def createMenu(self,category):
        readData = self.readDb.getMenu(category)
        for index in range(0, len(readData)):
            img_obj = QPixmap(readData[index]['p_img_url'])
            # img_obj.scaledToWidth(284)
            # img_obj.scaledToHeight(177)
            self.image_list[index].setPixmap(img_obj)
            self.name_list[index].setText(readData[index]['p_name'])
            self.name_list[index].setFont(QtGui.QFont("굴림", 15))

            self.price_list[index].setText(str(readData[index]['p_price']))
            self.price_list[index].setFont(QtGui.QFont("굴림", 15))

            # 람다식의 참조 변수를 변화시키기 위해 하드코딩
            if index == 0:
                data0 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data0]))
            elif index == 1:
                data1 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data1]))
            elif index == 2:
                data2 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data2]))
            elif index == 3:
                data3 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data3]))
            elif index == 4:
                data4 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data4]))
            elif index == 5:
                data5 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data5]))
            elif index == 6:
                data6 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data6]))
            elif index == 7:
                data7 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.showDialog(readData[data7]))

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

            # 람다식의 참조 변수를 변화시키기 위해 하드코딩
            if index == 0:
                data00 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data00]))
            elif index == 1:
                data01 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data01]))
            elif index == 2:
                data02 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data02]))
            elif index == 3:
                data03 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data03]))
            elif index == 4:
                data04 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data04]))
            elif index == 5:
                data05 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data05]))
            elif index == 6:
                data06 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data06]))
            elif index == 7:
                data07 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(lambda: self.noneMethod(readData[data07]))


    #  위젯 클릭 이벤트 Util
    def clickable(self,widget):
        class Filter(QObject):
            clicked = pyqtSignal()
            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            return True
                return False
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    # 레이아웃 제거 Util
    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def boxdelete(self, box):
        for i in range(self.order_list_layout.count()):

            layout_item = self.order_list_layout.itemAt(i)
            if layout_item.layout() == box:
                self.deleteItemsOfLayout(layout_item.layout())
                self.order_list_layout.removeItem(layout_item)
                break




    def createDialog(self):
        return Menu.CartDialog(self)

    class CartDialog(QDialog, dialog_form_class):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            QDialog.__init__(self, outer_instance)
            self.setupUi(self)

            self.btn_putCart.clicked.connect(lambda : self.addCart())
            self.count_plus.clicked.connect(lambda  : self.countPlus())
            self.count_minus.clicked.connect(lambda: self.countMinus())



        def setProduct(self,row_data):
            self.row_data = row_data

            # 이미지
            img_obj = QPixmap(self.row_data['p_img_url'])
            self.dialog_Image_label.setPixmap(img_obj)

            # 상품명
            self.product_name.setText(self.row_data['p_name'])
            # 상품 가격
            self.product_price.setText(str(self.row_data['p_price']))
            # 총가격
            self.product_total_price.setText(str(self.row_data['p_price']))

            self.product_price.setFont(QtGui.QFont("굴림", 15))
            # 삼풍 설명
            self.product_detail.setText(self.row_data['p_detail'])


            # 영양 성분표 데이터 split
            nutirition_str = str(self.row_data['p_nutrition'])
            split_str = nutirition_str.split('/')
            print(split_str)

            product_weight          = split_str[0]
            product_kcal            = split_str[1]
            product_carbohydrate    = split_str[2]
            product_protein         = split_str[3]
            product_transFat        = split_str[4]
            product_salt            = split_str[5]



            self.nutritopn_weight.setText(product_weight + "g")
            self.nutritopn_kcal.setText(product_kcal + "kcal")
            self.nutritopn_carbohydrate.setText(product_carbohydrate + "g")
            self.nutritopn_protein.setText(product_protein + "g")
            self.nutritopn_transfat.setText(product_transFat + "mg")
            self.nutritopn_salt.setText(product_salt + "mg")

        def countPlus(self):
            count = int(self.product_count.text()) + 1
            total_price = self.row_data['p_price'] * count

            self.product_count.setText(str(count))
            self.product_total_price.setText(str(total_price))

        def countMinus(self):
            if int(self.product_count.text()) - 1 > 0 :
                count = int(self.product_count.text()) - 1
                total_price = self.row_data['p_price'] * count
                self.product_count.setText(str(count))
                self.product_total_price.setText(str(total_price))

        def addCart(self):

            self.outer_instance.addOrder(self.row_data["p_name"], int(self.product_count.text()), self.row_data["p_price"])
            self.close()

        def showModal(self):
            return super().exec_()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Menu()

    myWindow.show()
    app.exec_()