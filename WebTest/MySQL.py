import pymysql


class MySQLConnect:
    def __init__(self, host=None, name=None, pwd=None, table=None):
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
    hj_test_cust = MySQLConnect(host="", name="", pwd="", table="")
    hj_test_ulog = MySQLConnect(host="", name="", pwd="", table="")
    hj_test_portal = MySQLConnect(host="", name="", pwd="", table="")
    hj_pre_cust = MySQLConnect(host="", name="", pwd="", table="")
    hj_pre_portal = MySQLConnect(host="", name="", pwd="", table="")
    hj_test_cust.sql_execute("SELECT * FROM tf_f_cust_group where cust_id=3019040314013175")
    # hj_test_cust.sql_execute("show rule from tf_f_cust_group")
    hj_test_ulog.sql_execute('''select a.REQ_JSON,a.RESP_JSON,a.LOG_TIME from operation_log a 
where class_name="com.ztesoft.bss.cust_capacity.wsdl.endpoint.CUSBUCUGrpAccountSerEndpoint" and a.method_name="crtGrpAccountInfo"
and a.LOG_TIME BETWEEN '2019-04-04 00:00:00'  and  '2019-04-05 18:00:00';''')
