import pymysql, pymongo

class LagouSQL(object):

    def lagou_mysql(self):
        config = {'host': 'localhost', 'user': 'root', 'password': '1234', 'db': 'employee', 'charset': 'utf8mb4'}
        connection = pymysql.connect(**config)
        # connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
        with connection.cursor() as cursor:
            sql = 'select * from lagou_shanghai'
            cursor.execute(sql)
            results = cursor.fetchall()
            for i, row in enumerate(results, 1):
                print(i, row)

    def lagou_mongodb(self):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['employee']
        lagou = db['lagou']
        for i, row in enumerate(db.lagou.find({}), 1):
            print(i, row)

if __name__ == '__main__':
    sql = LagouSQL()
    # sql.lagou_mysql()
    sql.lagou_mongodb()