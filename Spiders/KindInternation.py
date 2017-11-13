# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetWebContent
import GetHTML

href_list = ['http://news.ifeng.com/listpage/11574/0/1/rtlist.shtml'];


def catchInterNation(cursor, conn):
    for href in href_list:
        currenthref = href;
        '''开始循环页面'''
        count = 0;
        while currenthref != '' \
                and currenthref != 'javascript:void(0);' \
                and currenthref != "javascript:alert('没有了');" \
                and count < 100:
            htmlcode = GetHTML.getHtml(currenthref);
            soup = BeautifulSoup(htmlcode, "html.parser");
            li_list = soup.find_all('div', class_='newsList')[0].find_all('li');
            for li in li_list:
                #print 'InterNation:',count, ':', li.a.get('href');
                GetWebContent.catch(unicode(li.a.get('href')), 'InterNation', cursor, conn);

            div_nextpage = soup.find_all('div', id='backDay');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].a.get('href');
            else:
                currenthref = '';
            count += 1;
