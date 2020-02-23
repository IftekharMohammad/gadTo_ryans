# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GadtoRyansItem(scrapy.Item):
    website = scrapy.Field()
    gadget_name = scrapy.Field()
    category_name = scrapy.Field()
    brand_name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    gadget_url = scrapy.Field()
    specification = scrapy.Field()
