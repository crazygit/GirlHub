# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from sqlalchemy.exc import IntegrityError

from girls.items import GirlItem
from girls.models import get_session, Girl


class SQLAlchemyPipeline(object):
    def __init__(self, url):
        self.session = get_session(url)

    def close_spider(self, spider):
        self.session.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings['DATABASE_URL']
        )

    def process_item(self, item, spider):
        model_class = None
        if isinstance(item, GirlItem):
            model_class = Girl
        if model_class:
            self.save_item(item, spider, model_class)
        else:
            spider.logger.warning('Unhandled Item %s' % item)

        return item

    def save_item(self, item, spider, model_class):
        unique_column = model_class.get_unique_column()
        unique_condition = {
            unique_column: item[unique_column]
        }
        model = self.session.query(model_class).filter_by(**unique_condition).first()
        if model:
            model.init_or_update(item)
        else:
            model = model_class(item)
            self.session.add(model)
        try:
            self.session.commit()
        except IntegrityError as e:
            spider.logger.error("Save %s failed, %s" % (item, e))
            self.session.rollback()
            raise DropItem("Duplicate item %s" % model.get_identity())
        except Exception as e:
            self.session.rollback()
            spider.logger.error("Add %s failed, %s" % (item, e))
