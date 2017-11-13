#coding=utf-8
'''
从数据库读取数据，以及训练集、验证集、测试集的划分
@author: shaw, 2017-10-31
'''

# import MySQLdb
import Preprocess
import random
import numpy as np
import os
from xml.dom import minidom
from urlparse import urlparse
import codecs
import re
from xml.etree.ElementTree import parse


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DataIO():

    def __init__(self, outer_data_dir, data_size=10, mode=None):
        self.all_article_num = 0
        self.__all_data = {}
        self.__train_data = {}
        self.__eval_data_X = []
        self.__eval_data_y = []
        self.__test_data = []

        # database_data = self.__get_database_data(data_size)
        database_data = {}
        outer_data = self.__get_outer_data(outer_data_dir, data_size)
        # fenghuang_data = self.__get_outer_data('')
        self.__merge_all_data(outer_data, database_data)
        # self.__all_data = data

        if mode == 'nb':
            self.__split_data_nb()
        else:
            self.__split_data_scorss_val()


    def get_train_data(self):
        return self.__train_data

    def get_all_data(self):
        return self.__all_data

    def get_eval_data_X(self):
        return self.__eval_data_X

    def get_eval_data_y(self):
        return self.__eval_data_y

    def get_test_data(self):
        return self.__test_data

    # def __get_database_data(self, data_size):
    #     database_data = {}
    #     for i in range(1, Preprocess.class_num + 1):
    #         if i not in database_data:
    #             database_data[i] = []
    #
    #     conn = MySQLdb.connect(host="localhost", user='root',
    #                            passwd='wxx19941114', db="LEETCODE", charset="utf8mb4")
    #     cursor = conn.cursor()
    #     class_map = Preprocess.class_map2
    #     for i in range(1, Preprocess.class_num + 1):
    #         if i not in class_map:
    #             continue
    #         i_class = class_map[i]
    #         ## fetch all data from database of class i
    #         cursor.execute("SELECT article_content FROM web_page WHERE article_class = '%s';"
    #                            % i_class)
    #         i_class_articles = []
    #         ### ================================
    #         ### ======== 每类先取data_szie篇测试 ========
    #         ### ================================
    #         for row in cursor.fetchmany(data_size):
    #             article = Preprocess.process_single_page(row[0])
    #             i_class_articles.append(article)
    #         database_data[i] = i_class_articles
    #
    #     return database_data


    def __get_outer_data(self, outer_data_dir, data_szie):
        return Preprocess.process_all_articles(outer_data_dir, data_szie)


    def __merge_all_data(self, outer_data, database_data):
        if outer_data == None:
            outer_data = {}
        for i in range(1, Preprocess.class_num + 1):
            if i not in self.__all_data:
                self.__all_data[i] = []
        for i in range(1, Preprocess.class_num + 1):
            i_num = 0
            for data in outer_data[i]:
                self.__all_data[i].append(data)
                i_num += 1
            # if len(database_data) == 0:
            #     continue
            # for data in database_data[i]:
            #     self.__all_data[i].append(data)
            #     i_num += 1
            self.all_article_num += i_num
            print '====== Class %s has %s ======' % (Preprocess.class_map2[i], i_num)
        print '====== Data merge  done, all data length : %s ======' % self.all_article_num
        print ''


    def __split_data_nb(self, enough = False):
        '''
        训练集文档数:>=500000篇;每类平均50000篇。
        测试集文档数:>=500000篇;每类平均50000篇。
        '''
        class_map = Preprocess.class_map2
        eval_tmp = {}
        for i in range(1, Preprocess.class_num + 1):
            if i not in eval_tmp:
                eval_tmp[i] = []
        tmp_X = []
        tmp_y = []
        if enough == True:
            for i in range(1, Preprocess.class_num + 1):
                self.__train_data[i] = self.__all_data[i][0: 500000]
                eval_tmp[i] = self.__all_data[i][50000: ]

            for y, X in eval_tmp.items():
                tmp_y.append(y)
                tmp_X.append(X)

            np.random.seed(10)
            shuffle_indices = np.random.permutation(np.range(len(tmp_y)))
            self.__eval_data_y = tmp_y[shuffle_indices]
            self.__eval_data_X = tmp_X[shuffle_indices]

            # test_tmp.append(self.__test_data[i][50000: 1000000])
            # for test in test_tmp:
            #     for t in test:
            #         self.__test_data.append(t)
            # random.shuffle(self.__test_data)
        else:
            for i in range(1, Preprocess.class_num + 1):
                if i not in self.__train_data:
                    self.__train_data[i] = []

            n_split = int((self.all_article_num / Preprocess.class_num) * 0.9)
            for i in range(1, Preprocess.class_num + 1):
                self.__train_data[i] = self.__all_data[i][0: n_split]
                eval_tmp[i] = self.__all_data[i][n_split: ]

            for y in eval_tmp.keys():
                for x in eval_tmp[y]:
                    tmp_y.append(y)
                    tmp_X.append(x)
            self.__eval_data_y = tmp_y
            self.__eval_data_X = tmp_X

            # np.random.seed(10)
            # shuffle_indices = np.random.permutation(np.arange(len(tmp_y)))
            # self.__eval_data_y = tmp_y[shuffle_indices]
            # self.__eval_data_X = tmp_X[shuffle_indices]

            #     test_tmp.append(self.__all_data[i][n_split: len(self.__all_data)])
            # for test in test_tmp:
            #     for t in test:
            #         self.__test_data.append(t)
            # random.shuffle(self.__test_data)


    def __split_data_scorss_val(self, enough = False):

        pass


    def gen_outer_source_data(self):
        data_dir = '../data/sougo2'
        outer_dir = '../data/outer_sougo/'
        self.__outer_data_helper(data_dir, outer_dir)


    def __outer_data_helper(self, file_dir, out_path):

        new_file_dir = 'data/new_sougo2'
        if not os.path.exists(new_file_dir):
            os.makedirs(new_file_dir)

        dicurl = {'it.sohu.com': '科技', 'sports.sohu.com': '体育',
                  'cul.sohu.com': '文艺', 'mil.news.sohu.com': '军事', 'yule.sohu.com': '娱乐'}
        ## 改变文件编码格式
        # for root, dirs, files in os.walk(file_dir):
        #     for i_file in files:
        #         if i_file == '.DS_Store':
        #             continue
        #         print i_file
        #         file_path = os.path.join(file_dir, i_file)
        #         new_file_out_path = os.path.join(new_file_dir, i_file)
        #         with codecs.open(file_path, 'r', encoding='gb18030') as f:
        #             tmp = f.read()
        #
        #         with codecs.open(new_file_out_path, 'w', encoding='utf-8') as f:
        #             f.write(tmp)

        ## 使用正则表达式找url和content
        for root, dirs, files in os.walk(new_file_dir):
            i = 0
            for f in files:
                i += 1
                f_path = os.path.join(new_file_dir, f)
                with codecs.open(f_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip().encode('utf-8') for line in f.readlines()]
                    url_pattern = re.compile(r'(?<=<url>)(.*?)(?=</url>)')
                    content_pattern = re.compile(r'(?<=<content>)(.*?)(?=</content>)')
                    lines = ' '.join(lines)
                    url_lines = url_pattern.findall(lines)
                    content_lines = content_pattern.findall(lines)
                    print '====== Dealing %sth file... ======' % i, len(url_lines), len(content_lines)
                    for url, content in zip(url_lines, content_lines):
                        url_parse = urlparse(url)
                        if dicurl.has_key(url_parse.hostname):
                            out_file_path = os.path.join(out_path, dicurl[url_parse.hostname])
                            if not os.path.exists(out_path + dicurl[url_parse.hostname]):
                                os.makedirs(out_file_path)
                            fp_in = file(out_file_path + "/%d.txt" % (
                                            len(os.listdir(out_file_path)) + 1), "w")
                            fp_in.write(content.encode('utf8'))


if __name__ == '__main__':
    pass
    # dataio = DataIO('../data/outer_sougo')
    # dataio.gen_outer_source_data()
