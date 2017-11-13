
# -*- coding: UTF-8 -*-
import re;

from bs4 import BeautifulSoup;

import GetWebContent;
import GetHTML;

href_list = ['http://finance.ifeng.com/macro/',
             'http://finance.ifeng.com/gold/inews/index.shtml',
             'http://finance.ifeng.com/wemoney/list/index.shtml'];

href_home = ['http://finance.ifeng.com/stock/',
             'http://finance.ifeng.com/money/',
             'http://finance.ifeng.com/'];

def catchEco(cursor, conn):
    for href in href_list:
        currenthref = href;
        '''开始循环页面'''
        count = 0;
        while currenthref != '' \
                and currenthref != 'javascript:void(0);' \
                and currenthref != "javascript:alert('没有了');" \
                and count < 200:
            htmlcode =GetHTML.getHtml(currenthref);
            soup = BeautifulSoup(htmlcode, "html.parser");
            detail_list = soup.find_all('h3');
            for h in detail_list:
                #print 'Economy:',h.a.get('href');
                GetWebContent.catch(unicode(h.a.get('href')), 'Economy', cursor, conn);

            div_nextpage = soup.find_all('a', class_="a_ts02");
            if div_nextpage.__len__() != 0:
                currenthref = div_nextpage[0].get('href');
            else:
                currenthref = '';

            count += 1;

    for href in href_home:
        htmlcode = GetHTML.getHtml(href);
        soup = BeautifulSoup(htmlcode, "html.parser");
        list1 = soup.find_all('a', href=re.compile('http://finance.ifeng.com/a/'));
        for item in list1:
            if unicode(item.get("href"))[0] == 'h':
                #print 'Economy:',item.get("href");
                GetWebContent.catch(unicode(item.get('href')), 'Economy',cursor, conn);
