# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Scraped date -> item Containers -> Json, csv, xml
# Scraped date -> item Containers -> Pineline -> SQL / Mongo database

import sqlite3

class FollowersPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("Overwatch.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        # self.curr.execute("""DROP TABLE IF EXISTS user_db""")
        self.curr.execute("""create table IF NOT EXISTS user_db(
                Id INTEGER UNIQUE,
                Label INTEGER UNIQUE,
                FOLLOWERS INTEGER,
                view_count INTEGER
                )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert or ignore into user_db values (?,?,?,?)""", (
            item['ID'],
            item['USER'],
            item['FOLLOWERS'],
            item['view_count']
        ))
        self.conn.commit()
