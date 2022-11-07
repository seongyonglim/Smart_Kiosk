import sys

from PyQt5.QtCore import QSize, pyqtSignal, QEvent, QObject, Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import copy
from util.ReadDataBase import ReadDB

form_class = uic.loadUiType("./resources/menu.ui")[0]

dialog_form_class = uic.loadUiType("./resources/cart_dialog.ui")[0]

form_class2 = uic.loadUiType("./resources/simple_payment.ui")[0]

form_class3 = uic.loadUiType("./resources/cart_view.ui")[0]
form_class4 = uic.loadUiType("./resources/card_insert.ui")[0]

class Menu(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.readDb = ReadDB()

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
        self.image_list = [self.product_image_1, self.product_image_2, self.product_image_3, self.product_image_4,
                           self.product_image_5, self.product_image_6, self.product_image_7, self.product_image_8]
        # 상품 이름 리스트
        self.name_list = [self.product_name_1, self.product_name_2, self.product_name_3, self.product_name_4,
                          self.product_name_5, self.product_name_6, self.product_name_7, self.product_name_8]
        # 상품 가격 리스트
        self.price_list = [self.product_price_1, self.product_price_2, self.product_price_3, self.product_price_4,
                           self.product_price_5, self.product_price_6, self.product_price_7, self.product_price_8]

        ###########################################
        # 카테고리 버튼 생성
        self.createCategoryButton()
        # 카테고리 1 메뉴 로드
        self.createMenu(1)
        print("MenuView")
        self.all_cancle_button.clicked.connect(
            lambda: self.delete_order_all())

        # 결제
        self.simple_payment = CartView(self)

        self.order_button.clicked.connect(self.doPay)

    def doPay(self):
        self.order_total_price_cal()
        print(">", self.total_price)
        self.showPaymentDialog(str(self.total_price))

    def createCategoryButton(self):
        for cur in range(0, len(self.category_name_list)):
            category_button = QPushButton(self.category_name_list[cur])
            category_button.setFixedSize(QSize(121, 71))
            self.category_button_list.append(category_button)
            self.category_button_layout.addWidget(category_button)

        self.category_button_list[0].clicked.connect(
            lambda: self.createMenu(0))
        self.category_button_list[1].clicked.connect(
            lambda: self.createMenu(1))
        self.category_button_list[2].clicked.connect(
            lambda: self.createMenu(2))
        self.category_button_list[3].clicked.connect(
            lambda: self.createMenu(3))

    def addOrder(self, order_name, count, price):
        order_widgets_list = []
        orderHB = QHBoxLayout()
        orderHB.addStretch(8)

        # 주문하기 위젯 생성
        order_no_label = QLabel(str(len(self.order_layout_list) + 1))
        order_name_label = QLabel(order_name)

        order_num_plus_btn = QPushButton("+")
        order_count_label = QLabel(str(count))
        order_num_minus_btn = QPushButton("-")

        order_price_label = QLabel(str(price))
        order_price_total = QLabel(str(count * price))

        order_cancle_btn = QPushButton("X")

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
        order_num_plus_btn.clicked.connect(
            lambda: self.order_count_plus(order_widgets_list))
        order_num_minus_btn.clicked.connect(
            lambda: self.order_count_minus(order_widgets_list))
        order_cancle_btn.clicked.connect(
            lambda: self.order_delete(order_widgets_list))

        self.order_list_layout.addLayout(orderHB)
        self.order_layout_list.append(order_widgets_list)

        self.order_total_price_cal()

    ##########################################################
    # 주문 리스트의 버튼 시작
    ##########################################################
    def order_count_plus(self, args):
        order_count_label = args[4]
        order_price_label = args[6]
        order_total_label = args[7]

        text = order_count_label.text()
        text = str(int(text) + 1)
        total = str(int(text) * int(order_price_label.text()))

        order_count_label.setText(text)
        order_total_label.setText(total)

        self.order_total_price_cal()

    def order_count_minus(self, args):
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

    def order_delete(self, args):
        order_no_label = args[1]
        no = int(int(order_no_label.text()) - 1)

        self.boxdelete(self.order_layout_list[no][0])
        del self.order_layout_list[no]

        for i in range(0, len(self.order_layout_list)):
            self.order_layout_list[i][1].setText(str(i+1))
        self.order_total_price_cal()

    def delete_order_all(self):
        size = len(self.order_layout_list)
        for no in range(size):
            self.boxdelete(self.order_layout_list[0][0])
            del self.order_layout_list[0]

            for i in range(0, len(self.order_layout_list)):
                self.order_layout_list[i][1].setText(str(i+1))
        self.order_total_price_cal()

    # 총 금액 계산
    def order_total_price_cal(self):
        total_price = 0
        for i in range(0, len(self.order_layout_list)):
            total_price += int(self.order_layout_list[i][7].text())
        self.total_price_label.setText(str(total_price))
        self.total_price = total_price

    ##########################################################
    # 주문 리스트의 버튼 끝
    ##########################################################

    def showDialog(self, data):
        self.cartDialog.setProduct(data)
        self.cartDialog.showModal()

    def noneMethod(self):
        1 == 1

    def createMenu(self, category):
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
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data0]))
            elif index == 1:
                data1 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data1]))
            elif index == 2:
                data2 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data2]))
            elif index == 3:
                data3 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data3]))
            elif index == 4:
                data4 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data4]))
            elif index == 5:
                data5 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data5]))
            elif index == 6:
                data6 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data6]))
            elif index == 7:
                data7 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.showDialog(readData[data7]))

        for index in range(len(readData) + 1, 9):
            index = index - 1
            img_obj = QPixmap("./resources/etc/default.jpg")
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
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data00]))
            elif index == 1:
                data01 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data01]))
            elif index == 2:
                data02 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data02]))
            elif index == 3:
                data03 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data03]))
            elif index == 4:
                data04 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data04]))
            elif index == 5:
                data05 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data05]))
            elif index == 6:
                data06 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data06]))
            elif index == 7:
                data07 = copy.deepcopy(index)
                self.clickable(self.image_list[index]).connect(
                    lambda: self.noneMethod(readData[data07]))

    #  위젯 클릭 이벤트 Util
    def clickable(self, widget):
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
    def deleteItemsOfLayout(self, layout):
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

            self.btn_putCart.clicked.connect(lambda: self.addCart())
            self.count_plus.clicked.connect(lambda: self.countPlus())
            self.count_minus.clicked.connect(lambda: self.countMinus())

        def setProduct(self, row_data):
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

            product_weight = split_str[0]
            product_kcal = split_str[1]
            product_carbohydrate = split_str[2]
            product_protein = split_str[3]
            product_transFat = split_str[4]
            product_salt = split_str[5]

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
            if int(self.product_count.text()) - 1 > 0:
                count = int(self.product_count.text()) - 1
                total_price = self.row_data['p_price'] * count
                self.product_count.setText(str(count))
                self.product_total_price.setText(str(total_price))

        def addCart(self):

            self.outer_instance.addOrder(self.row_data["p_name"], int(
                self.product_count.text()), self.row_data["p_price"])
            self.close()

        def showModal(self):
            return super().exec_()

    def showPaymentDialog(self, price):
        self.simple_payment.showModal()

class CartView(QMainWindow, form_class3):
    def __init__(self, outer_instance):
        self.outer_instance = outer_instance
        QDialog.__init__(self, outer_instance)
        self.setupUi(self)

        self.simple_payment = self.Simple_payment(self)
        self.vlayout = self.vertical_main_layout
        self.vlayout_list = []
        self.product_list = []
        self.scrollArea.setLayout(self.vlayout)

        data = [{'p_no': 2, 'p_name': '더블버거\t', 'p_price': 4500, 'p_category': 1, 'p_detail': '더블 버거',
                 'p_img_url': './resources/hamburger/doubleburger.jpg',
                 'p_detail_img_url': './resources/hamburger/doubleburger.jpg', 'p_nutrition': '312/390/38/20/0/752'},
                {'p_no': 6, 'p_name': '핵폭탄버거', 'p_price': 12000, 'p_category': 1, 'p_detail': '고칼로리 수제버거',
                 'p_img_url': './resources/hamburger/핵폭탄버거.jpg',
                 'p_detail_img_url': './resources/hamburger/핵폭탄버거.jpg',
                 'p_nutrition': '650/1707/50/105/120.8/50/3067'},
#                {'p_no': 1, 'p_name': '불고기버거\t', 'p_price': 4000, 'p_category': 1, 'p_detail': '불고기 소스를 이용한 버거',
#                 'p_img_url': './resources/hamburger/bulgogiburger.jpg',
#                 'p_detail_img_url': './resources/hamburger/bulgogiburger.jpg',
#                 'p_nutrition': '158/380/380/18/0/0/523'},
#                {'p_no': 5, 'p_name': '푸짐버거', 'p_price': 8000, 'p_category': 1, 'p_detail': '양이 푸짐한 햄버거',
#                 'p_img_url': './resources/hamburger/푸짐버거.jpg', 'p_detail_img_url': './resources/hamburger/푸짐버거.jpg',
#                'p_nutrition': '315/780/115/37/19/0/1368'},
                {'p_no': 3, 'p_name': '콜라', 'p_price': 2000, 'p_category': 2, 'p_detail': '콜라',
                'p_img_url': './resources/drink/콜라.jpg',
                'p_detail_img_url': './resources/drink/콜라.jpg',
                'p_nutrition': '650/1707/50/105/120.8/50/3067'},
                ]

        for index in data:
            self.addProduct(index,1)
        self.getPaymentPrice()

        self.paymeny_btn.clicked.connect(lambda :self.showDialog())

        #print(self.payment_btn)
        count_plus_btn = QPushButton("x")

    def showModal(self):
        self.show()

    def showDialog(self):
        print("show modal")
        self.simple_payment.showModal()
    def addProduct(self, row_data, count):
        # 상품명,
        # 상품가격
        vlayout = QVBoxLayout()

        product_name_label  = QLabel(row_data['p_name'])
        product_price_label = QLabel(str(row_data['p_price']))

        product_name_label.setFont(QtGui.QFont("굴림", 15))
        product_price_label.setFont(QtGui.QFont("굴림", 15))

        product_name_label.setAlignment(Qt.AlignCenter)
        product_price_label.setAlignment(Qt.AlignCenter)

        # 상품명       이미지
        # 상품가격
        hlayout = QHBoxLayout()

        product_image_label = QLabel('')
        img_obj = QPixmap(row_data['p_img_url'])
        product_image_label.setPixmap(img_obj)

        vlayout.addWidget(product_name_label)
        vlayout.addWidget(product_price_label)

        hlayout.addLayout(vlayout)
        hlayout.addWidget(product_image_label)

        # 수량     +  수  -
        count_layout = QHBoxLayout()

        count_str       = QLabel("수량")
        count_plus_btn  = QPushButton("+")
        count_label     = QLabel(str(count))
        count_minus_btn = QPushButton("-")

        count_str.setFont(QtGui.QFont("굴림", 15))
        count_plus_btn.setFont(QtGui.QFont("굴림", 15) )
        count_minus_btn.setFont(QtGui.QFont("굴림", 15))
        count_label.setFont(QtGui.QFont("굴림", 15))

        count_str.setAlignment(Qt.AlignCenter)
        count_label.setAlignment(Qt.AlignCenter)

        count_plus_btn.resize(20,20)
        count_minus_btn.resize(20, 20)

        count_layout.addWidget(count_str)
        count_layout.addWidget(count_plus_btn)
        count_layout.addWidget(count_label)
        count_layout.addWidget(count_minus_btn)


        # 합계 금액             0원
        total_price_layout  = QHBoxLayout()
        total_str           = QLabel("합계")
        total_price_label   = QLabel(str( (row_data['p_price'] * count))+ "원")

        total_str.setFont(QtGui.QFont("굴림", 15))
        total_price_label.setFont(QtGui.QFont("굴림", 15))

        total_str.setAlignment(Qt.AlignCenter)
        total_price_label.setAlignment(Qt.AlignCenter)

        total_price_layout.addWidget(total_str)
        total_price_layout.addWidget(total_price_label)

        # 상품명        이미지
        # 상품가격
        # 수량       +  수  -
        # ------------------
        # 합계 금액        0원
        product_vLayout = QVBoxLayout()

        product_vLayout.addLayout(hlayout)
        product_vLayout.addLayout(count_layout)
        line = QLabel('--------------------------------------------------------------------------------------------------------------------')
        line.setAlignment(Qt.AlignCenter)
        product_vLayout.addWidget(line)
        product_vLayout.addLayout(total_price_layout)
        line2 = QLabel('====================================================================================================================')
        line2.setAlignment(Qt.AlignCenter)
        product_vLayout.addWidget(line2)

        # 버튼 이벤트 선언
        args = []
        args.append(row_data)
        args.append(count_label)
        args.append(total_price_label)
        count_plus_btn.clicked.connect(lambda :self.countPlus(args))
        count_minus_btn.clicked.connect(lambda: self.countMinus(args))

        # 리스트에 위젯삽입
        list = []
        list.append(product_name_label)
        list.append(product_price_label)
        list.append(product_image_label)
        list.append(count_label)
        list.append(total_price_label)

        self.product_list.append(list)
        self.vlayout_list.append(product_vLayout)

        self.vlayout.addLayout(product_vLayout)

    def countPlus(self, args):
        row_data        = args[0]
        count_label     = args[1]
        total_label     = args[2]

        count = int(count_label.text()) + 1
        total = row_data['p_price'] * count

        count_label.setText(str(count))
        total_label.setText(str(total) + "원")
        self.getPaymentPrice()

    def countMinus(self, args):
        row_data = args[0]
        count_label = args[1]
        total_label = args[2]

        if (int(count_label.text()) - 1) > 0:
            count = int(count_label.text()) - 1
            total = row_data['p_price'] * count
            count_label.setText(str(count))
            total_label.setText(str(total) + "원")
            self.getPaymentPrice()

    def getPaymentPrice(self):
        total_price = 0
        for price in self.product_list:
            total_price += int(str(price[4].text())[0:(len((price[4].text())) -1)])
        self.payment_price.setText(str(total_price))


    class Simple_payment(QDialog, form_class4):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            QDialog.__init__(self, outer_instance)
            self.setupUi(self)

            img_obj = QPixmap("./resources/etc/card.jpg")
            self.card_image.setPixmap(img_obj)
        def showModal(self):
            print("payment")
            return super().exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Menu()

    myWindow.show()
    app.exec_()
