import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("./resources/cart_view.ui")[0]
form_class2 = uic.loadUiType("./resources/card_insert.ui")[0]

class CartView(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
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
                   {'p_no': 1, 'p_name': '불고기버거\t', 'p_price': 4000, 'p_category': 1, 'p_detail': '불고기 소스를 이용한 버거',
                 'p_img_url': './resources/hamburger/bulgogiburger.jpg',
                 'p_detail_img_url': './resources/hamburger/bulgogiburger.jpg',
                 'p_nutrition': '158/380/380/18/0/0/523'},
                {'p_no': 5, 'p_name': '푸짐버거', 'p_price': 8000, 'p_category': 1, 'p_detail': '양이 푸짐한 햄버거',
                 'p_img_url': './resources/hamburger/푸짐버거.jpg', 'p_detail_img_url': './resources/hamburger/푸짐버거.jpg',
                 'p_nutrition': '315/780/115/37/19/0/1368'}
                ]

        for index in data:
            self.addProduct(index,1)
        self.getPaymentPrice()

        self.paymeny_btn.clicked.connect(lambda :self.showDialog())

        print(self.payment_btn)
        count_plus_btn = QPushButton("x")

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


    class Simple_payment(QDialog, form_class2):
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
    cartView = CartView()
    cartView.show()
    app.exec_()
