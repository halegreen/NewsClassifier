
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetWebContent;
import GetHTML;
import time

href_list = ['http://ent.ifeng.com/listpage/3/1/list.shtml',
             'http://ent.ifeng.com/listpage/6/1/list.shtml'];

def catchEntertain(cursor, conn):
    for href in href_list:
        currenthref = href;
        '''开始循环页面'''
        count = 0;
        while currenthref != '' \
                and currenthref != 'javascript:void(0);' \
                and currenthref != "javascript:alert('没有了');" \
                and count < 500:
            htmlcode = GetHTML.getHtml(currenthref);
            soup = BeautifulSoup(htmlcode, "html.parser");
            h2_list = soup.find_all('h2');
            for h2 in h2_list:
                print 'Entertain:',h2.a.get('href');
                GetWebContent.catch(unicode(h2.a.get('href')), 'Entertain', cursor, conn);

            div_nextpage = soup.find_all('a', id='pagenext');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';
            count += 1;
