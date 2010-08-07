#!/usr/bin/env python

import pymongo
from datetime import datetime
from util import slugify, convert_datetime

class DataBaseException(Exception):
    pass

class Database(object):

    def __init__(self):
        try:
            self.connection = pymongo.Connection()
        except:
            raise DataBaseException

        self.collection = self.connection.refer.posts

    def add_post(self, title, post, tags):
        url = slugify(title)
        self.collection.save(dict(title=title,
                                  post=post,
                                  tags=tags,
                                  comments=[],
                                  time=datetime.now(),
                                  url=url)
        )

    def add_comment(self, url, author, email, comment):
        post = self.collection.find_one(dict(url=url))
        post['comments'].append(dict(author=author,
                                     email=email,
                                     comment=comment,
                                     time=datetime.now())
        )
        self.collection.save(post)

    def get_posts(self):
        return map(convert_datetime, \
                    self.collection.find().sort('time', pymongo.DESCENDING))

    def get_post(self, url):
        return convert_datetime(self.collection.find_one(dict(url=url)))

    def search_for_tag(self, tag):
        return map(convert_datetime, \
            self.collection.find({'tags': tag}).sort('time', pymongo.DESCENDING))
