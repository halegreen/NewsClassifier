# -*- coding: UTF-8 -*-
import os
import re
import sys

import bs4
from bs4 import BeautifulSoup
import GetHTML

reload(sys)
sys.setdefaultencoding('utf-8')


def catch(url, kind, cursor, conn):
    """
    """
    try:
        if url == '':
            return
        htmlcode = GetHTML.getHtml(url)

        soup = BeautifulSoup(htmlcode, "html.parser")

        title_soup = soup.title
        topic = ''
        if title_soup != None:
            topic = unicode(title_soup.string)
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            topic = re.sub(rstr, "", topic)  # 消除非法字符
        else:
            return
        kind_name = getkindChineseName(kind)
        out_path = 'fenghaungnews'
        filepath = u"../data/%s/%s/" % (out_path, kind_name)

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        content = ''
        if kind == 'Sports_wemedia':
            for child in soup.find_all('div', class_="yc_con_txt")[0].descendants:
                if child.name == 'p' and child.string != None:
                    content = content + unicode(child.string)
        else:
            content_list = soup.find_all('div', id='main_content')
            if content_list == []:
                return

            for child in content_list[0].descendants:
                if child.string != None \
                        and unicode(child)[0] != '<' \
                        and type(child.string) != bs4.element.Comment \
                        and unicode(child.string) != '\n':
                    content = content + unicode(child.string) + u'\n'

        # cursor.execute("INSERT INTO web_page(article_class, article_content) VALUES(%s ,%s);",
        #                (kind_name.encode('utf-8'), content.encode('utf-8')))
        # conn.commit()

        with open(filepath + str(topic) + '.txt', 'w') as f:
            f.write(content)
        print kind_name, ' : ', url
        print

    except BaseException, e:
        dealException1(url, kind, e)



def dealException1(url, kind, e):
    errormessage = "error : " + e.message + "->" + url + "\n"
    LogPath = u"../output/"
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)
    with open(LogPath + "error.log", 'w') as f:
        f.write(errormessage)
    print errormessage


def dealException(url, kind):
    errormessage = "error : UnCatchedError->" + url + "\n"
    LogPath = u"../output/"
    if not os.path.exists(LogPath):
        os.makedirs(LogPath)
    with open(LogPath + "error.log", 'w') as f:
        f.write(errormessage)
    print errormessage


def getkindChineseName(kind):
    if kind == 'Sports_wemedia' or kind == 'Sports':
        return u'体育'
    else:
        if kind == 'Army':
            return u'军事'
        else:
            if kind == 'Entertain':
                return u'娱乐'
            else:
                if kind == 'History':
                    return u'历史'
                else:
                    if kind == 'Art':
                        return u'文艺'
                    else:
                        if kind == 'InterNation':
                            return u'国际'
                        else:
                            if kind == 'Society':
                                return u'社会'
                            else:
                                if kind == 'Tech':
                                    return u'科技'
                                else:
                                    if kind == 'Economy':
                                        return u'财经'
                                    else:
                                        if kind == 'InnerNation':
                                            return u'国内'
                                        else:
                                            return u'游戏'