# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import re


class MysqlHelper:
    def __init__(self, config):
        """
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
        if not self.con:
            self.con.close()
        else:
            print("数据库未连接")

    # 获取数据库版本号
    def get_version(self):
        self.cur.execute("SELECT VERSION()")
        return self.get_one_data()

    # 获取上个查询的结果
    def get_one_data(self):
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        return data

    def is_exist_table(self, tablename):
        """
        :param tablename: 表名
        :return: 表存在 True  表不存在 False
        """
        sql = "select * from %s" % tablename
        result = self.execute_commit(sql)
        print(result)
        if not result:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True

    def execute_commit(self, sql=''):
        """
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

    # 创建数据库表
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


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'database':'stockstar_spider',
        'charset':"utf8"
    }
    # 初始化打开数据库连接
    mydb = MysqlHelper(config)

    # 打印数据库版本
    print(mydb.get_version())

    # 创建表
    # TABLE_NAME = 'equity_funds_table'
    # print("========= 选择数据表%s ===========" % TABLE_NAME)
    # # CREATE TABLE %s(id int(11) primary key,name varchar(30))' %TABLE_NAME
    # attrdict = {'基金代码': 'int', "基金简称": 'varchar(50) NOT NULL', '单位净值': 'float', '累计净值': 'float', '日增长额': 'float', '日增长率': 'flost'}
    # constraint = 'PRIMARY KEY(`id`)'
    # mydb.create_table(TABLE_NAME, attrdict, constraint)

    TABLE_NAME = 'test_user2'
    print("========= 选择数据表%s ===========" % TABLE_NAME)
    # CREATE TABLE %s(id int(11) primary key,name varchar(30))' %TABLE_NAME
    attrdict = {'name': 'varchar(30) NOT NULL'}
    constraint = "PRIMARY KEY(`id`)"
    mydb.create_table(TABLE_NAME,attrdict,constraint)

