# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FollowersItem(scrapy.Item):
    # define the fields for your item here like:
    ID = scrapy.Field()
    USER = scrapy.Field()
    FOLLOWERS = scrapy.Field()
    view_count = scrapy.Field()

    pass
