# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pymysql


class MysqlHelper:
    def __init__(self, config):
        """
        配置数据库
        :param config: 配置
        构造方法：
            config = {
                 'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'passwd': 'root',
                'charset':'utf8',
            }
        """
        self.host = config["host"]
        self.username = config["user"]
        self.password = config["passwd"]
        self.port = config["port"]
        self.database = config["database"]
        self.con = None
        self.cur = None

        try:
            self.con = pymysql.connect(**config)
            self.con.autocommit(1)
            self.cur = self.con.cursor()
        except Exception as e:
            print(e)
            print("数据库连接失败,请检查config配置.")

    # 关闭数据库
    def close(self):
        """关闭数据库"""
        if not self.con:
            self.con.close()
        else:
            print("数据库未连接")

    def get_version(self):
        """获取数据库版本号"""
        self.cur.execute("SELECT VERSION()")
        return self.get_one_data()

    def get_one_data(self):
        """获取上个查询的结果"""
        data = self.cur.fetchone()
        return data

    def is_exist_table(self, tablename):
        """
        检查数据库表是否存在
        :param tablename: 表名
        :return: 表存在 True  表不存在 False
        """
        sql = "select * from %s" % tablename
        result = self.execute_commit(sql)
        if not result:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True

    def execute_commit(self, sql=''):
        """
        执行sql语句
        :param sql: sql语句
        :return: 针对更新,删除,事务等操作失败时回滚
        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print("error:", error)
            return error

    def execute_sql(self, sql=''):
        """执行sql语句，针对读操作返回结果集
            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except pymysql.Error as e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)
            return None

    def create_table(self, tablename, attrdict, constraint):
        """创建数据库表

            args：
                tablename  ：表名字
                attrdict   ：属性键值对,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：主外键约束,PRIMARY KEY(`id`)
        """
        if self.is_exist_table(tablename):
            print("%s is exit" % tablename)
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr, value in attrdict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print('creatTable:' + sql)
        self.execute_commit(sql)

    def insert(self, tablename, params):
        """
        插入数据
        :param tablename: 数据库表名
        :param params: {key(属性键): value(属性值)}
        :return:
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            key.append(tmpkey)
            if isinstance(tmpvalue, str):
                value.append("\'{}\'".format(tmpvalue))
            else:
                value.append(tmpvalue)
        attrs_sql = "({})".format(','.join(key))
        values_sql = "values({})".format(','.join(value))
        sql = "insert into {}".format(tablename)
        sql = sql + attrs_sql + values_sql
        print('_insert:' + sql)
        self.execute_commit(sql)

    def select(self, tablename, cond_dict='', order='', fields='*'):
        """查询数据

            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件

            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + '`' + k + '`' + '=' + '"' + v + '"' + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                print("fields input error, please input list fields.")
        sql = sql + consql + order
        print('select:' + sql)
        return self.execute_sql(sql)


'''
if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'database': 'stockstar_spider',
        'charset': "utf8"
    }
    # 初始化打开数据库连接
    mydb = MysqlHelper(config)

    # 打印数据库版本
    print(mydb.get_version())

    # 创建表
    TABLE_NAME = 'equity_funds_table'
    print("========= 选择数据表%s ===========" % TABLE_NAME)
    attrdict = {
        'fund_code': 'varchar(30)',
        "fund_abbreviation": 'varchar(50) NOT NULL',
        "fund_abbreviation_link": 'varchar(300)',
        'net_unit_value': 'varchar(30)',
        'accumulated_net': 'varchar(30)',
        'daily_growth': 'varchar(30)',
        'daily_growth_rate': 'varchar(30)'
    }
    constraint = 'PRIMARY KEY(`id`)'
    mydb.create_table(TABLE_NAME, attrdict, constraint)
    # mydb.select(TABLE_NAME, cond_dict={"fund_code": "00001", "fund_abbreviation": "测试股票","fund_abbreviation_link":"www.baidu.com"}, order='', fields='*')
    mydb.insert(TABLE_NAME, params={"fund_code": "00001", "fund_abbreviation": "测试股票", "fund_abbreviation_link":"www.baidu.com"})
'''
