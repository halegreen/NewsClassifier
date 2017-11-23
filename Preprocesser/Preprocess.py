#encoding=utf-8
'''
Preprocess text data.
@author: shaw, 2017-10-25
'''

import jieba
import jieba.posseg
import os
import codecs
import DataIO
from multiprocessing import Pool
import time
import dill as pickle
import gc

class_map = {'文艺' : 1, '财经' : 2, '科技' : 3, '娱乐': 4, '军事' : 5,
             '社会' : 6, '体育' : 7, '历史' : 8, '国际' : 9, '游戏' :10}

class_map2 = {1 : '文艺', 2 : '财经', 3 : '科技', 4 : '娱乐', 5 : '军事',
              6 : '社会', 7 : '体育', 8 : '历史', 9 : '国际', 10 : '游戏'}

class_map3 = {2 : '财经', 6 : '社会', 8 : '历史', 9 : '国际', 10 : '游戏'}

new_class_map = {"健康":1, "军事":2, "文化":3, "能源":4, "生活":5, "财经":6, "体育":7, "汽车":8, "娱乐":9, "科技":10}
new_class_map2 = {1:"健康", 2:"军事", 3:"文化", 4:"能源", 5:"生活", 6:"财经", 7:"体育", 8:"汽车", 9:"娱乐", 10:"科技"}

class_num = 10

filedir = 'utils/stop_words_ch.txt'

with codecs.open(filedir, 'r', encoding='GBK', errors='ignore') as f:
    stop_words = set([line.strip().encode('utf-8') for line in f.readlines()])


def get_data_from_database():
    dataio = DataIO.DataIO()
    all_articles = dataio.get_all_data()
    return all_articles


def process_single_page(page):
    sg_list = jieba.posseg.cut(page)
    res = [word.word for word in sg_list if word.flag == 'n' and word not in stop_words]
    # noun_words = [i.word.encode('utf-8') for i in sg_list if list(i.flag)[0] == 'n']
    # res = [word for word in noun_words if word not in stop_words]
    return res


def process_all_articles():
    all_articles = {}
    data_dir = '../data/all_data/jin_data/'
    out_data_dir = '../data/new_cuted_all_data/'
    ## 多进程进行文件分词
    # pool = Pool(processes=4)  

    for dir in os.listdir(data_dir):
        if dir == '.DS_Store':
            continue
        class_path = os.path.join(data_dir, dir)
        i_class = new_class_map[str(dir)]
        i_class_article = []
        print "====== Preprocessing  class: %s ======" % str(dir)
        s = time.time()
        ### ================================
        ### ==== 每类先取data_size篇测试 =====
        ### ================================
        i = 1
        i_class_article = []
        tmps = []
        for i_file in os.listdir(class_path):
            if i_file == '.DS_Store':
                continue
            article_path = os.path.join(class_path, i_file)
            print '---- Process %sth class_dir ----' % i
            tmp = multi_process(article_path)
            for t in tmp:
                tmps.append(t)
            del tmp
            gc.collect()
        #     tmp = pool.apply_async(multi_process, (article_path, ))
        #     tmps.append(tmp)
        # pool.close()
        # pool.join()
        i += 1
        i_class_article = [tmp for tmp in tmps]
        del tmps
        gc.collect()
        if not os.path.exists(out_data_dir):
                os.makedirs(out_data_dir)
        with open(out_data_dir + dir, 'wb') as f:
            pickle.dump(i_class_article, f, -1)
        del i_class_article
        gc.collect()
        e = time.time()
        print "======= Class %s finished, time consumed %s s ======" % (str(dir), (e - s))


def multi_process(article_path):
    jieba.enable_parallel()
    size = 0
    articles = []
    for ii_file in os.listdir(article_path):
        if ii_file == '.DS_Store':
            continue
        article_path_f = os.path.join(article_path, ii_file)
        with open(article_path_f, 'r') as f:
            i_file = f.read()
        print'---- processing %sth article ----' % size
        try:
            sg_list = jieba.posseg.cut(i_file)
            processed_article = [word.word for word in sg_list if word.flag == 'n' and word not in stop_words]
            ## 有些文章内容为空或者很短，应该排除
            if len(processed_article) < 20:
                continue
            articles.append(processed_article)
            size += 1
        except:
            print '**** 分词异常 ****'
            continue
    return articles


if __name__ == '__main__':
    pass




