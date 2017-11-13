
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetWebContent
import GetHTML

href_list = ['http://news.ifeng.com/listpage/4763/1/list.shtml',
             'http://news.ifeng.com/listpage/4764/1/list.shtml'];

def catchHistroy(cursor, conn):
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
                #print 'History:',count,':',t.a.get('href');
                GetWebContent.catch(unicode(t.a.get('href')), 'History', cursor, conn);

            div_nextpage = soup.find_all('a', id='pagenext');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';
            count += 1;