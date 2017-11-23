#coding=utf-8
import dill as pickle

class BaseModel(object):

    def __init__(self, all_articles):
        # print 'BaseModel init'
        # self.bow = BOW.BOW(feature_word_num=300, all_data=all_articles)  ##seems only used in naive bayes
        with open('data/bow.pkl', 'rb') as f:
            self.bow = pickle.load(f)
            
    def __train(self, train_data):
        raise NotImplementedError

    def __train_n(self, train_X, train_y):
        raise NotImplementedError

    def __eval(self, predicts, eval_data_y):
        raise NotImplementedError

    def __predict(self, eval_data_X):  ## 单篇文章
        raise NotImplementedError