import pymysql


class MySQLConnect:
    def __init__(self, host="10.124.147.173", name="hj_test_cust", pwd="Test3333", table="hj_test_cust"):
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
    sql.sql_execute("SELECT * FROM tf_f_cust_group where cust_id = 16")
    sql.sql_execute("SELECT t.column_name '字段名',"
                    "t.COLUMN_TYPE '数据类型',"
                    "t.IS_NULLABLE '可为空',"
                    "t.COLUMN_KEY '主键',"
                    "t.COLUMN_DEFAULT '默认值',"
                    "t.COLUMN_COMMENT '注释'"
                    " FROM information_schema.COLUMNS t WHERE table_schema = 'hj_test_cust' AND table_name = 'tf_f_cust_group'")

