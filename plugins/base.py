#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import time
import re

class Source (object) :

    def __init__ (self):
        self.T = tools.Tools()
        self.now = int(time.time() * 1000)

    def getSource (self) :
        urlList = []

        url = 'https://www.jianshu.com/p/2499255c7e79'
        req = [
            'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
        ]
        res = self.T.getPage(url, req)

        if res['code'] == 200 :
            pattern = re.compile(r"<code(.*?)</code>", re.I|re.S)
            tmp = pattern.findall(res['body'])

            pattern = re.compile(r"#EXTINF:0,(.*?)\n#EXTVLCOPT:network-caching=1000\n(.*?)\n", re.I|re.S)

            sourceList = pattern.findall(tmp[0])
            sourceList = sourceList + pattern.findall(tmp[1])

            for item in sourceList :
                i = 1
                print('Checking[' + str(i) + ']:' + str(item[0]))
                i = i + 1
                netstat = self.T.chkPlayable(item[1])

                if netstat > 0 :
                    info = self.T.fmtTitle(item[0])

                    data = {
                        'title'  : str(info['id']) if info['id'] != '' else str(info['title']),
                        'url'    : str(item[1]),
                        'quality': str(info['quality']),
                        'delay'  : netstat,
                        'level'  : str(info['level']),
                        'online' : 1,
                        'udTime' : self.now,
                    }
                    urlList.append(data)
                else :
                    pass # MAYBE later :P
        else :
            pass # MAYBE later :P

        return urlList
