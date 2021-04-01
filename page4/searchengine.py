#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Time    : 2019/7/15 10:45
@Author  : Hou hailun
@File    : searchengine.py
"""

print(__doc__)

"""
本章: 搜索与排名 searching and ranking
搜索引擎的组成:
    step1: 搜索文档并保存
    step2：查询
"""

import sqlite3
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

# 构建一个单词列表，这些单词将被忽略
ignorewords = {'the': 1, 'of': 1, 'to': 1, 'and': 1, 'a': 1, 'in': 1, 'is': 1, 'it': 1}


class crawler:
    # 用于检索网页，创建数据库，以及建立索引

    def __init__(self, dbname):
        # 初始化crawler类并传入数据库名称
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    # 辅助函数，用于获取条目id，并且如果条目不存在，将其加入数据库
    def getentryid(self, table, field, value, createnew=True):
        return None

    # 为每个网页建立索引
    def addtoindex(self, url, soup):
        print('Indexing %s' % url)

    # 从一个HTML网页中提取文字(不带标签的)
    def gettextonly(self, soup):
        v = soup.string
        if v is None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # 根据任何非空白字符进行分词处理
    def separateword(self, text):
        return None

    # 如果url已经建立索引，则返回True
    def isindexed(self, url):
        return False

    # 添加一个关联两个网页的连接
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth=2):
        """
        爬虫程序
        :param pages: url集合
        :param depth: 指定爬取的深度
        :return:
        """
        for i in range(depth):
            newpages = set()
            print(pages)
            for page in pages:  # 广度优先遍历
                try:
                    c = request.urlopen(page)
                except:
                    print('Could not open %s' % page)
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)  # 为网页建立索引

                links = soup('a')
                for link in links:
                    url = parse.urljoin(page, link['href'])  # urljoin: url join函数
                    if url.find("'") != -1:
                        continue
                    url = url.split('#')[0]  # 去掉位置部分
                    if url[0:4] == 'http' and not self.isindexed(url):  # http且没有建立索引
                        newpages.add(url)
                    linkText = self.gettextonly(link)
                    self.addlinkref(page, url, linkText)

                self.dbcommit()
            pages = newpages

    # 创建表和索引
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()


if __name__ == "__main__":
    craw = crawler('searchindex.db')
    pagelist = ['http://kiwitobes.com/wiki/Perl.html']
    craw.crawl(pagelist)
    craw.createindextables()
