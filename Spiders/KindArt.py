# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetHTML
import GetWebContent

href_list = ['http://culture.ifeng.com/listpage/59665/1/list.shtml',
             'http://culture.ifeng.com/listpage/59666/1/list.shtml'];

def catchArt(cursor, conn):
    print 'catch art'
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
            title_list = soup.find_all('div',class_='box_list clearfix');
            for t in title_list:
                #print 'Art:',t.a.get('href');
                GetWebContent.catch(unicode(t.a.get('href')), 'Art', cursor, conn)

            div_nextpage = soup.find_all('a', id='pagenext');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';
            count += 1;

