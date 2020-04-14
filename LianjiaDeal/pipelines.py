# -*- coding: utf-8 -*-


from LianjiaDeal.items import LianjiadealItem
from LianjiaDeal.items import SpiderErrorItem
import pymongo

class MongoPipeline(object):
    def __init__(self,mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[LianjiadealItem.collection].create_index([('id', pymongo.ASCENDING)])


    def process_item(self, item, spider):
        if isinstance(item,LianjiadealItem):
            self.db[item.collection].update({'name': item.get('name'),'time': item.get('time')}, {'$set': item}, True)

        return item
    def close_spider(self, spider):
        self.client.close()

class SpiderErrorFile(object):

    def open_spider(self, spider):
        self.file = open(str(spider.name) + ".txt", "a")

    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        if isinstance(item,SpiderErrorItem):
            self.file.write(item)
            self.file.write('\n')