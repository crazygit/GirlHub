# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from girls.items import GirlItem
from girls.loader import GirlItemLoader


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={'parse_tags': True})

    def parse(self, response):
        page = response.meta.get('page', 1)
        category = response.meta.get('category', '美女')
        self.logger.info("解析列表页: %s, 页数: %s <%s>" % (category, page, response.url))

        # parse list
        for selector in response.css('ul.wp-list li.wp-item h3 a'):
            url = selector.xpath('./@href').extract_first()
            title = selector.xpath('.//text()').extract_first()

            yield Request(
                url=url,
                callback=self.parse_detail,
                meta={
                    'page': page,
                    'title': title,
                    'category': category,
                },
                priority=10
            )

        # parse next page
        next_page = response.xpath('//div[@id="wp_page_numbers"]//a[contains(.//text(), "下一页")]/@href').extract_first()
        if next_page:
            page = next_page.split('_')[-1].split('.')[0]
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                dont_filter=True,
                meta={
                    'page': page,
                    'category': category
                }
            )

        # parse tags
        if response.meta.get('parse_tags', False):
            tags = response.css('div.tags a')
            for tag_selector in tags:
                tag_url = tag_selector.xpath('./@href').extract_first()
                tag_title = tag_selector.xpath('./@title').extract_first()
                yield Request(
                    url=response.urljoin(tag_url),
                    callback=self.parse,
                    dont_filter=True,
                    meta={
                        'page': 1,
                        'category': tag_title
                    }
                )

    def parse_detail(self, response):
        self.logger.info("解析详情页: %s <%s>" % (response.meta.get('title', ''), response.url))
        l = GirlItemLoader(GirlItem(), response)
        l.add_css('title', 'div.metaRight h2 a::text')
        l.add_css('tags', 'div.metaRight p::text')
        l.add_css('day', 'div.metaLeft div.day::text')
        l.add_css('month_year', 'div.metaLeft div.month_Year::text')
        l.add_css('image_urls', 'div.postContent p img::attr(src)')
        l.add_value('url', response.url)
        l.add_value('category', response.meta.get('category', '美女'))
        return l.load_item()
