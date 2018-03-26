# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MoviesItem(scrapy.Item):
    mid = scrapy.Field()
    mname = scrapy.Field()
    mname2 = scrapy.Field()
    mactor = scrapy.Field()
    mintroduce = scrapy.Field()
    mscore = scrapy.Field()
    mupdatedate = scrapy.Field()
    mlength = scrapy.Field()
    mstartdate = scrapy.Field()
    mdirector = scrapy.Field()
    mlanguage = scrapy.Field()
    marea = scrapy.Field()
    mtype = scrapy.Field()
    mlink = scrapy.Field()