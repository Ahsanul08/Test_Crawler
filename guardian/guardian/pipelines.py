# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import re
from nltk import SnowballStemmer
from nltk.corpus import stopwords


class MongoPipeline(object):

    collection_name = 'news'
    non_word_regex = re.compile(r'\W+', re.UNICODE)

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.stemmer = SnowballStemmer('english')
        self.stop_words = stopwords.words('english')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def extract_keywords(self, content):
        content_tokens = set(self.non_word_regex.split(content.lower()))
        keywords = set()
        for token in content_tokens:
            stemmed_token = self.stemmer.stem(token)
            if stemmed_token and stemmed_token not in self.stop_words:
                keywords.add(stemmed_token)
        return list(keywords)


    def process_item(self, item, spider):
        item_as_dict = dict(item)
        content = item_as_dict.get('content')
        if content:
            item_as_dict['keywords'] = self.extract_keywords(content)
            self.db[self.collection_name].update_one(
                {
                    'url': item_as_dict['url']
                },
                {
                    '$setOnInsert': item_as_dict
                },
                upsert=True,
            )
        return item
