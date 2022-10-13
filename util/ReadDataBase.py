import pymysql

class ReadDB :
    def __init__(self):
        self.mysqldb = pymysql.connect(
            user='root',
            password='1234',
            host='127.0.0.1',
            port=3307,
            db='kiosk_DB',
            charset='utf8')

        # Dict형식의 CURSOR
        self.cursor = self.mysqldb.cursor(pymysql.cursors.DictCursor)


    def getMenu(self,category):
        sql = "SELECT * FROM kiosk_db.product WHERE p_category ='" + str(category) + "';"
        self.cursor.execute(query=sql)

        result = self.cursor.fetchall()
        return result

    def getAllMenu(self):
        sql = "SELECT * FROM kiosk_db.product;"
        self.cursor.execute(query=sql)

        result = self.cursor.fetchall()
        return result
if __name__ == "__main__" :
    readDb = ReadDB()
    result = readDb.getMenu()
