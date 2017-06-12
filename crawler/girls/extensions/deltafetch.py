# -*- coding: utf-8 -*-

import logging
import os
import time

from scrapy import Request, signals
from scrapy.exceptions import NotConfigured
from scrapy_deltafetch import DeltaFetch

from girls.models import Girl, get_session

logger = logging.getLogger(__name__)


class SyncDeltaFetch(object):
    def __init__(self, df, url):
        self.df = df
        self.session = get_session(url)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('SYNC_DELTAFETCH_ENABLED'):
            raise NotConfigured
        df = DeltaFetch.from_crawler(crawler)
        url = crawler.settings['DATABASE_URL']
        ext = cls(df, url)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)

        return ext

    def spider_opened(self, spider):
        if not os.path.exists(self.df.dir):
            os.makedirs(self.df.dir)
        dbpath = os.path.join(self.df.dir, '%s.db' % spider.name)
        if os.path.exists(dbpath):
            logger.info("Remove origin deltafetch db: %s" % dbpath)
            os.remove(dbpath)
        db = self.df.dbmodule.DB()
        try:
            db.open(filename=dbpath,
                    dbtype=self.df.dbmodule.DB_HASH,
                    flags=self.df.dbmodule.DB_CREATE)
            rows = self.get_rows_in_db(spider)
            for row in rows:
                key = self.df._get_key(Request(url=row.url))
                db[key] = str(time.time())
            logger.info("Sync %d records to %s" % (len(rows), dbpath))
        finally:
            db.close()

    def get_rows_in_db(self, spider):
        return self.session.query(Girl.url).all()

    def close_spider(self, spider):
        self.session.close()
