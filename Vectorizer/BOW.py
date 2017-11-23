#coding=utf-8
'''
Bag Of Words model for text classification task.
@author: shaw, 2017-10-26
'''

import math
# from sklearn.feature_extraction.text import CountVectorizer
import numba
from numba import autojit, jit
import gc
from multiprocessing import Pool
import dill as pickle
import pandas as pd
from collections import Counter


class BOW(object):

    def __init__(self, feature_word_num, all_data):
        self.article_num = 0
        self.class_num = len(all_data.keys())
        self.feature_word_num = feature_word_num  ## num of the most relative between the word and the class
        self.all_articles = all_data
        self.all_article_feat = []
        self.all_features = set()
        self.__TF_IDF_val = {}
        self.feat_helper = {}    ## 记录每一类中出现这个词的文档的数目
        self.article_word_dict = {}

        self.main()

    def main(self):
        print '====== Create dict... ======'
        self.create_dict()
        print '====== Reduce dimension... ======'
        self.reduce_dimension()


    def choose_feature(self, article, all_pages, article_idx):
        tmp_dict = {}
        # pool = Pool(processes=5)
        for word in article:
            if word in tmp_dict:
                continue
            else:
                # pool.apply_async(self.getTF_IDF, (word, all_pages, article_idx, ))
                tmp_dict[word] = self.getTF_IDF(word, all_pages, article_idx)
        # pool.close()
        # pool.join()
        return tmp_dict

    def getTF_IDF(self, word, all_pages, article_idx):
        # print 'word %s , tf: %.6f, idf: %.6f ' % (word, self.getTF(word, article_idx), self.getIDF(word))
        if word in self.__TF_IDF_val.keys():
            return
        self.__TF_IDF_val[word] = self.getTF(word, all_pages, article_idx) * self.getIDF(all_pages, word)

    @autojit
    def getTF(self, word, all_pages, article_idx):
        cnt = 0
        word_list = all_pages[article_idx]
        for w in word_list:
            if w == word:
                cnt += 1
                # print 'cnt %s' % cnt
        return float(cnt) / len(word_list)

    @autojit
    def getIDF(self, all_pages, word):
        df = 0
        for article in all_pages:
            if word in article:
                df += 1
        if df == 0:
            df = 1
        return math.log(self.article_num / df)

    def create_dict(self):
        concat_feat = []
        all_pages = []
        for i in range(1, 11):
            self.feat_helper[i] = {}
        for key in self.all_articles.keys():
            for v in self.all_articles[key]:
                all_pages.append(v)
        self.article_num = len(all_pages)
        print '====== All articles num: %s ===== ' % self.article_num

        for i_class, articles in self.all_articles.items():
            tmp_feat = set()
            concat_feat = []
            for article in articles:
                tmp_feat |= set(article)
                s_feat = set(article)
                for feat in s_feat:
                    concat_feat.append(feat)
        
            self.article_word_dict[i_class] = tmp_feat  ## word set for every class

            self.all_features |= tmp_feat

            self.feat_helper[i_class] = Counter(concat_feat)  ## 记录每一类中出现这个词的文档的数目
       

    def build_df_data(self):
        data = {}
        df = pd.DataFrame(data, index=range(1,11), columns=[word for word in self.all_features])
        cols = list(df.columns)
        # for i in range(1, 11):
        #     for col in cols:
        #         df = df.apply(lambda x: self.__feat_helper[i][col] if col in self.__feat_helper[i] else 0)
        # cols = list(df.columns)
        # print ' '.join(cols)  
        # print(df.head())
        # print('--- df shape: {} ---'.format(df.shape))
        return df

    def reduce_dimension(self):
        ## use chi-square test to reduce dimension of the article word dict
        self.all_features = self.chi_square_test()
        print '====== Feature dimension is : %s ======' % len(self.all_features)

    def chi_square_test(self):
        ## for every word, cacculate the chi_square value with the class it belongs to.
        @jit(nogil=True)
        def get_chi(word, i_class):
            A = 0
            B = 0
            C = 0
            D = 0
            cur_class_articles = self.all_articles[i_class]
            for article in cur_class_articles:
                if word in article:
                    A += 1
                else:
                    C += 1
            for class_num in range(1, self.class_num + 1):
                if class_num == i_class:
                    continue
                else:
                    articles = self.all_articles[class_num]
                    for article in articles:
                        if word in article:
                            B += 1
                        else:
                            D += 1
            if ((A + B) == 0 or (C + D) == 0):
                chi_value = 0
            else:
                chi_value = ((A * D - B * C) * (A * D - B * C)) / ((A + B) * (C + D))
            return chi_value

        def get_chi_fast(word, i_class):
            '''
            速度优化后的卡方检验
            '''
            A = 0
            if word in self.feat_helper[i_class]:
                A = self.feat_helper[i_class][word]
            C = (self.article_num / self.class_num) - A
            B = 0
            for i in range(1, 11):
                if i == i_class:
                    continue
                if word in self.feat_helper[i]:
                    B += self.feat_helper[i][word]
            D =  (self.article_num - (self.article_num / self.class_num)) - B

            if ((A + B) == 0 or (C + D) == 0):
                chi_value = 0
            else:
                chi_value = ((A * D - B * C) * (A * D - B * C)) / ((A + B) * (C + D))
            return chi_value


        res = set()
        for i_class, words in self.article_word_dict.items():
            class_feat = {}
            for word in words:
                # chi_value = get_chi(word, i_class)
                chi_value1 = get_chi_fast(word, i_class)
                # print('chi_value: %s, chi_value1: %s' % (chi_value, chi_value1))
                class_feat[word] = chi_value1

            class_feat = sorted(class_feat.items(), key=lambda x: x[1], reverse=True)  ## sort chi_value
            tmp_list = [k[0] for k in class_feat]

            if self.feature_word_num != -1:
                tmp_list = tmp_list[0: self.feature_word_num]
            # print ' '.join(tmp_list)
            res |= set(tmp_list)
        return res

    def vectorize(self):
        for article_idx in range(0, self.article_num):
            tmp_vec = [0 for i in range(len(self.all_features))]
            article_feat = self.all_article_feat[article_idx]
            vec_idx = 0
            for word in self.all_features:
                if word in article_feat.keys():
                    tmp_vec[vec_idx] = article_feat[word]
                    # print 'word %s in feat, tf-idf is : %.6f ' % (word, article_feat[word])
                    # print tmp_vec
                vec_idx += 1
            self.vec_article.append(tmp_vec)
            # print len(tmp_vec)

    def skl_bow(self, article, class_name):
        '''
        using sklearn
        '''
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(article).toarray()




if __name__ == '__main__':
    feat = 500 ## can be tuned
    pass


