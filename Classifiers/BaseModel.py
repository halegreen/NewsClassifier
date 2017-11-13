#coding=utf-8
from Vectorizer import BOW


class BaseModel(object):

    def __init__(self, all_articles):
        # print 'BaseModel init'
        # self.bow = BOW.BOW(feature_word_num=300, all_data=all_articles)  ##seems only used in naive bayes
        pass

    def __train(self, train_data):
        pass

    def __train_n(self, train_X, train_y):
        pass

    def __eval(self, predicts, eval_data_y):
        pass

    def __predict(self, eval_data_X):  ## 单篇文章
        pass