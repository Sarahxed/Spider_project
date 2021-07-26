# Name:  data_storage
# Purpose: 
# 
# @Author: Sarah
# Copyright:
# Licence:
#
# Created: 2019/11/28
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
from sqlalchemy import Column, Table, MetaData
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sunlight_administration_site.config import MYSQL_URL

engine = create_engine(MYSQL_URL)  # 定义引擎
metadata = MetaData(bind=engine)  # 绑定元信息

Base = declarative_base()
# Base.metadata.create_all(engine)


class Sunlight(Base):
    __tablename__ = "complain_table"
    id = Column(Integer, primary_key=True)
    url = Column(String(300), comment="链接")
    record = Column(Integer, comment="编号")
    title = Column(String(200), comment="主题")
    status = Column(String(20), comment="状态")
    netizen = Column(String(60), comment="网名")
    time = Column(String(60), comment="时间")


class Spider(object):
    def __init__(self):
        self.table = Table("complain_table", metadata, autoload=True)

    def insert(self, url, record, title, status, netizen, time):
        self.table.insert().values(url=url, record=record, title=title, status=status, netizen=netizen, time=time).execute()


if __name__ == '__main__':
    sun = Sunlight()
#     # 创建映射数据表(如果不存在)
    Base.metadata.create_all(engine)

