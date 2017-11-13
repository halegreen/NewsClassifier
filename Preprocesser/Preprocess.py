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

class_map = {'文艺' : 1, '财经' : 2, '科技' : 3, '娱乐': 4, '军事' : 5,
             '社会' : 6, '体育' : 7, '历史' : 8, '国际' : 9, '游戏' :10}

class_map2 = {1 : '文艺', 2 : '财经', 3 : '科技', 4 : '娱乐', 5 : '军事',
              6 : '社会', 7 : '体育', 8 : '历史', 9 : '国际', 10 : '游戏'}

class_map3 = {2 : '财经', 6 : '社会', 8 : '历史', 9 : '国际', 10 : '游戏'}

class_num = 10

filedir = 'utils/stop_words_ch.txt'

with codecs.open(filedir, 'r', encoding='GBK', errors='ignore') as f:
    stop_words = [line.strip().encode('utf-8') for line in f.readlines()]


def get_data_from_database():
    dataio = DataIO.DataIO()
    all_articles = dataio.get_all_data()
    return all_articles


def process_single_page(page):
    sg_list = jieba.posseg.cut(page)
    noun_words = [i.word.encode('utf-8') for i in sg_list if list(i.flag)[0] == 'n']
    # print ' '.join(noun_words)
    res = [word for word in noun_words if word not in stop_words]
    # print ' '.join(res)
    return res


def process_all_articles(data_dir, data_size):
    all_articles = {}
    for dir in os.listdir(data_dir):
        if dir == '.DS_Store':
            continue
        class_path = os.path.join(data_dir, dir)
        i_class = class_map[str(dir)]
        i_class_article = []
        print "====== Preprocessing  class: %s ======" % str(dir)
        ### ================================
        ### ======== 每类先取data_size篇测试 ========
        ### ================================
        size = 0
        for i_file in os.listdir(class_path):
            if i_file == '.DS_Store':
                continue
            article_path = os.path.join(class_path, i_file)
            with open(article_path, 'r') as f:
                i_file = f.read()
                processed_article = process_single_page(i_file)
                ## 有些文章内容为空或者很短，应该排除
                if len(processed_article) < 20:
                    continue
                i_class_article.append(processed_article)
                size += 1
                if size == data_size:
                    break
                # print ' '.join(processed_article)
        all_articles[i_class] = i_class_article

    return all_articles


if __name__ == '__main__':
    pass




