import pymysql

def sql_lagou():

    config = {'host': 'localhost', 'user': 'root', 'password': '1234', 'db': 'employee', 'charset': 'utf8mb4'}
    connection = pymysql.connect(**config)
    # connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')

    with connection.cursor() as cursor:
        sql = 'select * from lagou_shanghai'
        cursor.execute(sql)
        results = cursor.fetchall()
        for i, row in enumerate(results, 1):
            print(i, row)

if __name__=='__main__':
    sql_lagou()