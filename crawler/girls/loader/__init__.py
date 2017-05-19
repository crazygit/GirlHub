# -*- coding: utf-8 -*-

import logging

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst, Identity

from girls.loader.processors import Strip, RemoveGirlTag, FormatMonthYear

logger = logging.getLogger(__name__)


class BaseItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_fallback_css(self, field_name, css, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_css(field_name, css, *processors, **kw)

    def add_fallback_xpath(self, field_name, xpath, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, xpath, *processors, **kw)

    def add_fallback_value(self, field_name, xpath, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_value(field_name, xpath, *processors, **kw)


class GirlItemLoader(BaseItemLoader):
    tags_in = RemoveGirlTag()
    tags_out = Compose(TakeFirst(), Strip())
    month_year_in = FormatMonthYear()
    image_urls_out = Identity()
