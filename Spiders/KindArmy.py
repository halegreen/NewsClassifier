# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetWebContent
import GetHTML

href_list = ['http://news.ifeng.com/listpage/7129/1/list.shtml',
             'http://news.ifeng.com/listpage/7131/1/list.shtml',
             'http://news.ifeng.com/listpage/7130/1/list.shtml',
             'http://news.ifeng.com/listpage/7111/1/list.shtml'];
def catchArmy(cursor, conn):
    for href in href_list:
        currenthref = href;
        '''开始循环页面'''
        count = 0;
        while currenthref != '' \
                and currenthref != 'javascript:void(0);' \
                and currenthref != "javascript:alert('没有了');" \
                and count < 50:
            htmlcode = GetHTML.getHtml(currenthref);
            soup = BeautifulSoup(htmlcode, "html.parser");
            title_list = soup.find_all('div',class_='comListBox');
            for t in title_list:
                #print 'Army:',t.a.get('href');
                GetWebContent.catch(unicode(t.a.get('href')), 'Army', cursor, conn);

            div_nextpage = soup.find_all('a', id='pagenext');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';
            count += 1;