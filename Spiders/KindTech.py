# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup;

import GetHTML
import GetWebContent


def catchTech(cursor, conn):
    currenthref = 'http://tech.ifeng.com/listpage/803/1/list.shtml';
    '''开始循环页面'''
    count = 0;
    while currenthref != '' \
            and currenthref != 'javascript:void(0);' \
            and currenthref != "javascript:alert('没有了');" \
            and count < 70:
        htmlcode = GetHTML.getHtml(currenthref);
        soup = BeautifulSoup(htmlcode, "html.parser");
        title_list = soup.find_all('div', class_='zheng_list pl10 box');
        for t in title_list:
            #print 'Tech:',t.a.get('href');
            GetWebContent.catch(unicode(t.a.get('href')), 'Tech', cursor, conn);

        div_nextpage = soup.find_all('a', id='pagenext');
        if div_nextpage.__len__() != 0:
            currenthref = div_nextpage[0].get('href');
        else:
            currenthref = '';
        count += 1;


    currenthref = 'http://tech.ifeng.com/listpage/26334/1/list.shtml';
    '''开始循环页面'''
    count = 0;
    while currenthref != '' \
            and currenthref != 'javascript:void(0);' \
            and currenthref != "javascript:alert('没有了');" \
            and count < 50:
        htmlcode = GetHTML.getHtml(currenthref);
        soup = BeautifulSoup(htmlcode, "html.parser");
        title_list = soup.find_all('div', class_='box_list clearfix');
        for t in title_list:
            #print 'Tech:',t.a.get('href');
            GetWebContent.catch(unicode(t.a.get('href')), 'Tech', cursor, conn);

        div_nextpage = soup.find_all('a', id='pagenext');
        if div_nextpage.__len__() != 0:
            currenthref = div_nextpage[0].get('href');
        else:
            currenthref = '';
        count += 1;
