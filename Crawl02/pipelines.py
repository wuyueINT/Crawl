# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
pipeline主要用于做数据存储
在这里可以拦截item
并对拦截的item进行操作
"""
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
# 这个类里提供了item转为其他文件格式的接口
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class Crawl02Pipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义的用于保存json文件的pipeline
    """
    # 用codecs创建以及打开文件
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    # 处理item，写成json的格式
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    # 关闭文件
    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    """
    调用scrapy提供的json exporter导出json文件
    """
    # 初始化文件，并开始任务
    def __init__(self):
        self.file = open('crawl02exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    # 关闭
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 对item进行操作
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class Crawl02ImagePipeline(ImagesPipeline):
    """
    自定义的用于保存图片的pipeline
    可以通过重载方法实现自己的逻辑
    """
    # 这里记得要return item，便于后续执行的pipeline继续对item进行处理
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_path_file = value.get("path")
            item["image_path"] = image_path_file
        return super().item_completed(results, item, info)


class MysqlPipeline(object):
    """
    将数据存储到数据库
    """
    def __init__(self):
        # self.conn = MySQLdb.connect('host', 'user', 'password', 'dbname', charset='utf-8', user_unicode=True)
        self.conn = MySQLdb.connect('localhost', 'root', '', 'aaa', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into aaa(type, company_cn, company_en, number, image, url_md5)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["type"], item["company_cn"], item["company_en"],
                                         item["number"], item["image"], item["url_md5"]))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    """
    利用Twisted异步容器实现myqal的插入操作
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into aaa(type, company_cn, company_en, number, image, url_md5)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["type"], item["company_cn"], item["company_en"],
                                    item["number"], item["image"], item["url_md5"]))
        return item
