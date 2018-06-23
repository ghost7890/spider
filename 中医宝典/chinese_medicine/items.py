# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChineseMedicineItem(scrapy.Item):
    ks_name = scrapy.Field()            # 科室名
    ks_url = scrapy.Field()             # 科室url
    sick_name = scrapy.Field()          # 疾病名
    sick_url = scrapy.Field()           # 疾病url
    sick_des = scrapy.Field()           # 疾病描述
    sick_res = scrapy.Field()           # 病因
    sick_sym = scrapy.Field()           # 症状
    sick_dia = scrapy.Field()           # 诊断
    sick_com = scrapy.Field()           # 并发症
    sick_tre = scrapy.Field()           # 治疗
    sick_part = scrapy.Field()          # 部位

