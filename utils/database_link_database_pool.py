# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  database_link)database_pool
# Purpose: 
# 
# @Author: Sarah
# Copyright:
# Licence:
#
# Created: 2019/11/27
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------

import pymysql
from DBUtils.PooledDB import PooledDB


class DatabaseConnection(object):
    host = ''
    user = ''
    password = ''
    db = ''
    charset = ''
    port = 3306
    cursorclass = pymysql.cursors.SSDictCursor

    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.charset = kwargs.get('charset')
        self.db = kwargs.get('db')
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=kwargs.get('maxconnections', 20),
            mincached=kwargs.get('maxconnections', 20),
            maxcached=0,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset=self.charset,
            cursorclass=self.cursorclass
        )

    @property
    def connect(self):
        return self.pool.connection()

    def __excute(self, sql):
        with self.connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result

    def _commit(self, connect=None):
        if connect:
            connect.commit()
        else:
            self.connect.commit()

    def insert(self, table, **kwargs):
        sql_template = 'INSERT INTO {0} ({1}) VALUES ({2})'
        keys = [k for k, v in kwargs.items()]
        sql = sql_template.format(table, ', '.join(keys), ', '.join(['%s' for i in range(len(keys))]))

        with self.connect.cursor() as cursor:
            cursor.execute(sql, tuple(kwargs[k] for k in keys))
            self._commit(cursor.connection)

        return sql % tuple(kwargs[k] for k in keys)

    def insert_or_update(self, table, **kwargs):
        sql_template = 'INSERT INTO {0} ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE {3}'
        keys = [k for k in kwargs.keys()]
        sql = sql_template.format(
            table,
            ', '.join(keys),
            ', '.join(['%s' for i in range(len(keys))]),
            '= %s, '.join(keys) + ' = %s',
        )

        with self.connect.cursor() as cursor:
            cursor.execute(sql, tuple(kwargs[k] for k in keys) * 2)
            self._commit(cursor.connection)

    def select(self, table, conditions=None, order=None, columns=None, iterate=False, limit_num=1000):
        if not columns:
            columns = ('*',)
        cond = self._build_condition(conditions or {})
        where_sql = 'WHERE ' + cond if cond else ''
        limit_sql = 'LIMIT {}'.format(limit_num) if limit_num else ''
        sql_template = 'SELECT {column} FROM {table} {where} {order} {limit};'
        sql_str = sql_template.format(
            column=','.join(columns),
            table=table,
            where=where_sql,
            order='ORDER BY {}'.format(order) if order else '',
            limit=limit_sql)
        if not iterate:
            with self.connect.cursor() as cursor:
                cursor.execute(sql_str)
                result = cursor.fetchall()
                self._commit(cursor.connection)
            return result
        # else:
        #     with self.connect.cursor() as cursor:
        #         print('===' * 10, sql_str)
        #         cursor.execute(sql_str)
        #         for row in cursor.fetchall_unbuffered():
        #             yield row
        #     self._commit()

    def update(self, table, conditions={}, **kwargs):
        where_sql = 'WHERE ' + self._build_condition(conditions) if self._build_condition(conditions) else ''

        sql_template = 'UPDATE {0} SET {1} {2};'
        keys = [k for k, v in kwargs.items()]
        sql = sql_template.format(table, '= %s, '.join(keys) + ' = %s', where_sql)

        with self.connect.cursor() as cursor:
            cursor.execute(sql, tuple(kwargs[k] for k in keys))
            self._commit(cursor.connection)

    def _build_condition(self, conditions):
        con_list = []
        for k, v in conditions.items():
            if v is None:
                con_list.append('{} IS NULL'.format(k))
            elif v == '__not__null':
                con_list.append('{} is NOT NULL'.format(k))
            elif v is False:
                con_list.append('{} = false'.format(k))
            elif v is True:
                con_list.append('{} = true'.format(k))
            elif type(v) == str:
                if v.startswith('not_equel_to__'):
                    con_list.append('{} != "{}"'.format(k, v.replace('not_equel_to__', '')))
                    # TODO: __gt, __gte, __lt, __lte ...
                else:
                    con_list.append('{} = "{}"'.format(k, v))
            elif type(v) in (int, float):
                con_list.append('{} = {}'.format(k, str(v)))
            elif type(v) in (list, tuple, set):
                if not v:
                    continue
                elif len(tuple(v)) > 1:
                    con_list.append('{} in {}'.format(k, str(tuple(v))))
                else:
                    con_list.append('{} in {}'.format(k, str(tuple(v)).replace(',', '')))
            else:
                raise Exception('can not solve this condition: {}: {}', k, str(v))
        return ' AND '.join(con_list)
