import pymysql


class MySQLConnect:
    def __init__(self, host="涉密未填写", name="涉密未填写", pwd="涉密未填写", table="涉密未填写"):
        self.host = host
        self.name = name
        self.pwd = pwd
        self.table = table

    def sql_execute(self, sql):
        db = pymysql.connect(self.host, self.name, self.pwd, self.table)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取字段名
            index = cursor.description
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                for c in range(0, len(index)):
                    print(str(index[c][0]) + ' = ' + str(row[c]))
        except:
            print('未查询到指定数据')
        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    sql = MySQLConnect()
    sql.sql_execute("SELECT * FROM t.tf_f_cust_group where '涉密未填写'")
