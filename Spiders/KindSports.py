
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetWebContent
import GetHTML

href_list = ['http://sports.ifeng.com/listpage/53609/1/list.shtml',
             'http://sports.ifeng.com/listpage/11246/1/list.shtml',
             'http://sports.ifeng.com/listpage/11244/1/list.shtml'];


def catchSports(cursor, conn):
    for href in href_list:
        currenthref = href;
        '''开始循环页面'''
        count = 0;
        while currenthref !=''\
            and currenthref != 'javascript:void(0);' \
            and currenthref != "javascript:alert('没有了');" \
            and count < 50:
            htmlcode = GetHTML.getHtml(currenthref);
            soup = BeautifulSoup(htmlcode, "html.parser");
            title_list = soup.find_all('div', class_='box_list clearfix');
            for t in title_list:
                #print 'Sports:',t.a.get('href');
                if unicode(t.a.get('href')).endswith('wemedia.shtml'):
                    GetWebContent.catch(unicode(t.a.get('href')), 'Sports_wemedia', cursor, conn);
                else:
                    GetWebContent.catch(unicode(t.a.get('href')), 'Sports', cursor, conn);

            div_nextpage = soup.find_all('a', id='pagenext');
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';
            count += 1;
