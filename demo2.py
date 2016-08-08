#!/usr/bin/python
# encoding=utf8


import requests
import re
import sys
import os


def start( url, filename_output):
    rule3 = re.compile(r'__biz=([^&]+).*?key=([^& ]+).*?uin=([^& ]+)')
    res = rule3.findall(url)
    if len(res) > 0 and len(res[0]) == 3 :
        biz = res[0][0]
        key = res[0][1]
        uin = res[0][2]
        print "\nbiz:" + biz + "\nkey:" + key + "\nuin:" + uin;
        result = get_history_list(biz, key, uin)
        print_result(result, filename_output)

    return result
    


def get_history_list(biz, key, uin):
    result = []
    frommsgid = ''
    count = 10

    rule1 = re.compile(r'"id":(\d+?),')
    rule2 = re.compile(r'title":"(.*?)".*?content_url":"(.*?)"')

    pre_url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&key=%s&uin=%s&f=json'
    pre_url = pre_url % (biz, key, uin)

    while True:
        if frommsgid == '':
            txt = ''
        else:
            txt = '&frommsgid={0}'.format(frommsgid)
        url = pre_url + '&count=' + str(count) + txt
        headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255'}
        r = requests.get(url, headers=headers)

        if 'no session' in r.content:
            print " * Please update the url in readlist.txt * "
            break


        print "\nUrl:"+url;
        cont = r.content
        cont = cont.replace('\"', '"')
        cont = cont.replace('\\', '')
        cont = cont.replace('amp;', '')

       

        rre = re.findall(rule2, cont)
        if len(rre) == 0:
            break
        else:
            for r in rre:
                title, url = r
                result.append([title, url])
                # print '['+title+']' + '('+url+')' + "     "

        data = re.findall(rule1, cont)
        frommsgid = data[-1]

    return result


def print_result(result, filename_output):
    with open(filename_output+'.md', 'w') as f:
        i = 0
        for r in result:
            title, url = r
            f.write('['+title+']' + '('+url+')' + "     \n")
            i = i+1
            if i%10 == 0:
                f.write('\n\n')
    
    with open(filename_output+'.html', 'w') as f:
        f.write("<!DOCTYPE html><html><head><title>"+filename_output+"</title></head><meta charset=\"UTF-8\"><body>\n")
        f.write("<h3>"+filename_output+"</h3>\n")
        i = 0
        for r in result:
            title, url = r
            f.write('<a href="' +url+ '">' +title+ '</a><br/>\n')
            i = i+1
            if i%10 == 0:
                f.write('<br/><br/>\n\n')
        f.write('</body></html>')




def print_reslist( namelist, reslist):
    listlen = len(namelist)
    with open('__All.md', 'w') as f:
        for cur in range(listlen):
            f.write("### " + name[cur] + "\n\n")
            i = 0
            for r in reslist[cur]:
                title, url = r
                f.write('['+title+']' + '('+url+')' + "     \n")
                i = i+1
                if i%10 == 0:
                    f.write('\n\n')


def main():
    namelist = []
    reslist = []
    print " input name, url\n"
    nameUrl = raw_input('> ')
    while len(nameUrl) > 0:
        res = nameUrl.split(",")
        if len(res) == 1 and res[0].strip() == "exit":
            break
        elif len(res) == 2:
            name = res[0].strip()
            url = res[1].strip()
            print name, url
            result = start(url, name)
            if len(result) != 0:
                namelist.append(name)
                reslist.append(result)
        else:
            print " input name, url\n"

        nameUrl = raw_input('> ')

    # print reslist
    # print_reslist(namelist, reslist)



def sum():
    files = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.md']
    for afile in files:
        shell = 'echo  "### ' + os.path.splitext(afile)[0] + ' \n" >> __all0.md'
        os.system(shell)
        shell = 'cat ' + afile + ' >> __all0.md'
        os.system(shell)




if __name__ == '__main__':
    main()
    sum()



















