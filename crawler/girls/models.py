# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, create_engine, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ModelMixin(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
    }
    id = Column(Integer, primary_key=True)

    def get_identity(self):
        raise NotImplementedError

    @staticmethod
    def get_unique_column():
        raise NotImplementedError

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    def parse_item(self, item):
        for column in self.columns:
            if column in item:
                setattr(self, column, item[column])


def get_session(url, echo=False):
    engine = create_engine(url, echo=echo)
    Session = sessionmaker(bind=engine)
    # create table
    Base.metadata.create_all(engine)
    return Session()


class Girl(Base, ModelMixin):
    __tablename__ = 'girl'

    id = Column(Integer, primary_key=True)
    category = Column(String(64), doc='分类')
    title = Column(String(64), doc='图片标题')
    tags = Column(String(256), doc='标签')
    publish_time = Column(Date, doc='发布时间')
    image_urls = Column(Text, doc='图片链接')
    image_paths = Column(Text, doc='图片下载路径')
    url = Column(String(256), nullable=False, unique=True, doc='爬取信息的链接')
    created_on = Column(DateTime, nullable=False, default=datetime.now, doc='爬取时间')

    def __init__(self, item):
        self.init_or_update(item)

    def init_or_update(self, item):
        self.parse_item(item)
        self.tags = ','.join(item.get('tags', []))
        self.publish_time = datetime.strptime(item.get('day') + ' ' + item.get('month_year'), '%d %m-%Y')
        self.image_urls = self.parse_images(item.get('images'), 'url')
        self.image_paths = self.parse_images(item.get('images'), 'path')
        self.created_on = datetime.now()

    def parse_images(self, images, field):
        urls = []
        for image in images:
            urls.append(image[field])
        return ','.join(urls)

    def get_identity(self):
        return "%s %s" % (self.title, self.url)

    @staticmethod
    def get_unique_column():
        return 'url'
