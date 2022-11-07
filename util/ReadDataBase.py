# import pymysql


class ReadDB:
    def __init__(self):
        self.data = [
            {'p_no': 6, 'p_name': '추천 1', 'p_price': 12000, 'p_category': 0, 'p_detail': '고칼로리 수제버거',
             'p_img_url': './resources/hamburger/핵폭탄버거.jpg',
             'p_detail_img_url': './resources/hamburger/핵폭탄버거.jpg',
             'p_nutrition': '650/1707/50/105/120.8/50/3067'},
            {'p_no': 5, 'p_name': '추천 2', 'p_price': 8000, 'p_category': 0, 'p_detail': '양이 푸짐한 햄버거',
             'p_img_url': './resources/hamburger/푸짐버거.jpg', 'p_detail_img_url': './resources/hamburger/푸짐버거.jpg',
             'p_nutrition': '315/780/115/37/19/0/1368'},
            {'p_no': 2, 'p_name': '더블버거\t', 'p_price': 4500, 'p_category': 1, 'p_detail': '더블 버거',
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
             'p_nutrition': '315/780/115/37/19/0/1368'},


            {'p_no': 2, 'p_name': '사이다\t', 'p_price': 2000, 'p_category': 2, 'p_detail': '사이다',
             'p_img_url': './resources/drink/사이다.jpg',
             'p_detail_img_url': './resources/drink/사이다.jpg', 'p_nutrition': '312/390/38/20/0/752'},
            {'p_no': 6, 'p_name': '콜라', 'p_price': 2000, 'p_category': 2, 'p_detail': '콜라',
             'p_img_url': './resources/drink/콜라.jpg',
             'p_detail_img_url': './resources/drink/콜라.jpg',
             'p_nutrition': '650/1707/50/105/120.8/50/3067'},

            {'p_no': 2, 'p_name': '감자튀김\t', 'p_price': 3000, 'p_category': 3, 'p_detail': '감자튀김',
             'p_img_url': './resources/side/potato.jpg',
             'p_detail_img_url': './resources/side/potato.jpg', 'p_nutrition': '312/390/38/20/0/752'},

        ]
        # self.mysqldb = pymysql.connect(
        #     user='root',
        #     password='1234',
        #     host='127.0.0.1',
        #     port=3307,
        #     db='kiosk_DB',
        #     charset='utf8')

        # # Dict형식의 CURSOR
        # self.cursor = self.mysqldb.cursor(pymysql.cursors.DictCursor)

    def getMenu(self, category):
        sql = "SELECT * FROM kiosk_db.product WHERE p_category ='" + \
            str(category) + "';"
        # self.cursor.execute(query=sql)

        # result = self.cursor.fetchall()
        data = []
        for menu in self.data:
            if menu["p_category"] == category:
                data.append(menu)
        return data

    def getAllMenu(self):
        # sql = "SELECT * FROM kiosk_db.product;"
        # self.cursor.execute(query=sql)

        return self.data


if __name__ == "__main__":
    readDb = ReadDB()
    result = readDb.getMenu()
