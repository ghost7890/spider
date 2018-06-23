# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import log
from scrapy.exceptions import DropItem


class ChineseMedicinePipeline(object):

    def __init__(self):

        self.getdb_settings()

        connection = pymongo.MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        db = connection[self.MONGO_DB]
        self.coll = db[self.MONGO_COLL]

        # 判断集合是否为空
        ret = self.coll.find()
        # 不为空，清空
        if ret.count() != 0:
            self.coll.remove()

        self.num = 1

    def getdb_settings(self):
        """
        从db_settings.txt读取设置好的数据库信息
        :return:
        """
        d = {}
        with open('db_settings.txt', 'rb') as f:
            db_settings = f.read().decode('utf-8').split('\n')

        for line in db_settings:
            if not line.strip():
                continue
            tmp = line.split(':')
            d[tmp[0].strip()] = tmp[1].strip()

        self.MONGO_HOST = d['MONGO_HOST']
        self.MONGO_PORT = int(d['MONGO_PORT'])
        self.MONGO_DB = d['MONGO_DB']
        self.MONGO_COLL = d['MONGO_COLL']




    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))
        if valid:

            print(str(self.num) + '. ' + item['sick_name'] + ' 信息已获取')

            self.num += 1
            self.coll.insert(dict(item))
            log.msg('question added to mongodb database!',
                    level=log.DEBUG, spider=spider)
        return item




