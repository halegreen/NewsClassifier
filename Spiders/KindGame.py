
# -*- coding: UTF-8 -*-
import re;

from bs4 import BeautifulSoup;

import GetWebContent
import GetHTML

href_home = ['http://games.ifeng.com/',
             'http://games.ifeng.com/yejiehangqing/index.shtml'];

def catchGames(cursor, conn):
    for href in href_home:
        htmlcode =GetHTML.getHtml(href);
        soup = BeautifulSoup(htmlcode, "html.parser");
        list1 = soup.find_all('a', href=re.compile('http://games.ifeng.com/a/'));
        for item in list1:
            if unicode(item.get("href"))[0] == 'h':
                #print 'Games:',item.get("href");
                GetWebContent.catch(unicode(item.get('href')), 'Games', cursor, conn);
