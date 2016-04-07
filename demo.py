#!/usr/bin/python
# encoding=utf8


import requests
import re
import sys

class WeiXin(object):
    def __init__(self, count=10, readlist='', filename_output=''):
        self.count = count
        self.readlist = readlist
        self.frommsgid = ''
        self.result = []
        self.filename_output = filename_output

    def start(self):
        with open(self.readlist, 'r') as f:
            lines = f.readlines()
        lines.reverse()
        p = re.compile(r'__biz=([^&]+).*?key=([^& ]+).*?uin=([^& ]+)')
        for l in lines:
            m = p.findall(l)
            if not m:
                continue
            self.biz = m[0][0]
            self.key = m[0][1]
            self.uin = m[0][2]
            break

        print "\nbiz:"+self.biz+"\nkey:"+self.key +"\nuin:"+self.uin;

        try:
            while True:
                self.get_history_list()
                # break
        except Exception, e:
            print "pass"
        finally:
            print "***  ***"

        self.print_result()


    def get_history_list(self):

        self.pre_url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&key=%s&uin=%s&f=json'
        self.pre_url = self.pre_url % (self.biz, self.key, self.uin)

        if self.frommsgid == '':
            txt = ''
        else:
            txt = '&frommsgid={0}'.format(self.frommsgid)
        url = self.pre_url + '&count=' + str(self.count) + txt
        headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255'}
        r = requests.get(url, headers=headers)

        if 'no session' in r.content:
            print " * Please update the url in readlist.txt * "
            raise Exception('***')

        print "\nUrl:"+url;
        cont = r.content
        cont = cont.replace('\"', '"')
        cont = cont.replace('\\', '')
        cont = cont.replace('amp;', '')

        data = re.findall(r'"id":(\d+?),', cont)
        self.frommsgid = data[-1]

        rre = re.findall(r'title":"(.*?)".*?content_url":"(.*?)"', cont)
        
        for r in rre:
            title, url = r
            self.result.append([title, url])
            # print '['+title+']' + '('+url+')' + "     "


    def print_result(self):
        with open(self.filename_output+'.md', 'w') as f:
            i = 0
            for r in self.result:
                title, url = r
                f.write('['+title+']' + '('+url+')' + "     \n")
                i = i+1
                if i%10 == 0:
                    f.write('\n\n')
        
        with open(self.filename_output+'.html', 'w') as f:
            f.write("<!DOCTYPE html><html><head><title>"+self.filename_output+"</title></head><meta charset=\"UTF-8\"><body>\n")
            f.write("<h3>"+self.filename_output+"</h3>\n")
            i = 0
            for r in self.result:
                title, url = r
                f.write('<a href="' +url+ '">' +title+ '</a><br/>\n')
                i = i+1
                if i%10 == 0:
                    f.write('<br/><br/>\n\n')
            f.write('</body></html>')



def main(filename_output):
    readlist = 'readlist.txt'
    wx = WeiXin(count=10, readlist=readlist, filename_output=filename_output)
    wx.start()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "ex: python demo.py Fenng"
