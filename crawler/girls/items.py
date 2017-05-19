# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GirlItem(scrapy.Item):

    # 分类
    category = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 图片链接
    image_urls = scrapy.Field()
    images = scrapy.Field()
    # 日期
    day = scrapy.Field()
    # 年月
    month_year = scrapy.Field()
    # 爬取的页面链接
    url = scrapy.Field()
