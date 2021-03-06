#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import db
import time
import re
from plugins import base
from plugins import lista
from plugins import dotpy

class Iptv (object):

    def __init__ (self) :
        self.T = tools.Tools()
        self.DB = db.DataBase()

    def run(self) :
        # Base = base.Source()
        # urlList = Base.getSource()
        # for item in urlList :
        #     self.addData(item)

        # listA = lista.Source()
        # urlList = listA.getSource()
        # for item in urlList :
        #     self.addData(item)

        Dotpy = dotpy.Source()
        urlList = Dotpy.getSource()
        for item in urlList :
            self.addData(item)

        self.outPut()
        print("DONE!!")

    def addData (self, data) :
        sql = "SELECT * FROM %s WHERE url = '%s'" % (self.DB.table, data['url'])
        result = self.DB.query(sql)

        if len(result) == 0 :
            data['enable'] = 1
            self.DB.insert(data)
        else :
            id = result[0][0]
            self.DB.edit(id, data)

    def outPut (self) :
        sql = """SELECT * FROM
            (SELECT * FROM %s WHERE online = 1 ORDER BY delay DESC) AS delay
            GROUP BY delay.title
            HAVING delay.title != '' and delay.title != 'CCTV-'
            ORDER BY level ASC, length(title) ASC, title ASC
            """ % (self.DB.table)
        result = self.DB.query(sql)

        with open('tv.m3u8', 'w') as f:
            f.write("#EXTM3U\n")
            for item in result :
                className = '其他频道'
                if item[4] == 1 :
                    className = '中央频道'
                elif item[4] == 2 :
                    className = '地方频道'
                elif item[4] == 3 :
                    className = '地方频道'
                else :
                    className = '其他频道'

                f.write("#EXTINF:-1, group-title=\"%s\", %s\n" % (className, item[1]))
                f.write("%s\n" % (item[3]))

obj = Iptv()
obj.run()





