# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiadealItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    collection = 'deal_2020_4_11'
    # 标题
    name = scrapy.Field()
    # 户型
    type = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 产权属性
    property = scrapy.Field()
    # 产权年限
    property_year = scrapy.Field()
    # 交易时间
    time = scrapy.Field()
    # 建成年代
    year = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 朝向
    direction = scrapy.Field()
    # 装修情况
    fitment = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 小区
    residential = scrapy.Field()
    # 电梯
    elevator = scrapy.Field()
    # 用途
    purpose = scrapy.Field()

class SpiderErrorItem(scrapy.Item):
    url = scrapy.Field()
    error_reason = scrapy.Field()