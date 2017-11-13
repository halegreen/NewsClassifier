# coding=utf-8
'''
Naive Bayes model for text classification task.
@author: shaw 2017-10-28
'''
import BaseModel
import numba
from sklearn import metrics
from sklearn.metrics import classification_report
import math

class NaiveBayes(BaseModel.BaseModel):

    def __init__(self, all_data):
        BaseModel.BaseModel.__init__(self, all_data)
        # print 'Naive Bayes init'
        self.__word_dict = {}
        self.__class_prob = {}

    @numba.jit()
    def __train(self, train_data):
        all_articles = train_data

        for feat in self.bow.all_features:
            if feat not in self.__word_dict:
                self.__word_dict[feat] = []

        ## for every word in dict, get prob of class1
        for i_class, articles in all_articles.items():
            self.__class_prob[i_class] = float(len(articles)) / self.bow.article_num
            for word in self.__word_dict.keys():
                nk = 0
                n = 0
                for article in articles:
                    for w in article:
                        if w == word:
                            nk += 1
                    n += len(article)
                prob = (nk + 1.0) / (n + len(self.bow.all_features))
                self.__word_dict[word].append(prob)  ## 得到word与第i类的似然


    def __eval(self, predicts, eval_data_y):
        '''
        :param predicts:
        :return: Accuracy, recall, and F1-SCORE,混淆矩阵
        '''
        if len(predicts) is not len(eval_data_y):
            print 'Error : Predicts dim %s is not equal to the eval_data_y dim %s!' \
                  % (len(predicts), len(eval_data_y))
        ## 每一类的正确率、召回率
        print(classification_report(eval_data_y, predicts))
        ## 总体的正确率、召回率、F-score
        all_acc = metrics.accuracy_score(eval_data_y, predicts)
        all_recall = metrics.recall_score(eval_data_y, predicts, average='micro')
        print ''
        print 'All class accuracy is %s, recall score is %s ' % (all_acc, all_recall)
        print ''
        print 'Confusion Matrix :'
        con_mat = metrics.confusion_matrix(eval_data_y, predicts)
        print con_mat


    def __predict(self, eval_data_X):
        predicts = []
        for data in eval_data_X:
            predicts.append(self.__predict_single(data))
        return predicts

    @numba.jit()
    def __predict_single(self, article):
        article_words = article
        post_probs = {}
        for i in range(1, self.bow.class_num + 1):
            likelihood = 1.0
            for word in article_words:
                # print likelihood
                if word in self.__word_dict:
                    likelihood += math.log(self.__word_dict[word][i - 1])
                else:
                    likelihood += math.log(1.0 / len(self.__word_dict.keys()))  ## 平滑

            post_probs[i] = self.__class_prob[i] * (likelihood)
            # print 'class_prob: %s, likelihood: %s' % (self.__class_prob[i], likelihood)

        res = sorted(post_probs.items(), key=lambda x: x[1], reverse=True)
        #print ' '.join(article[0:10]), '===> ', res
        return res[0][0]  ## 返回概率最大的那个类


    def train(self, train_data):
        self.__train(train_data)

    def eval(self, predicts, eval_data_y):
        return self.__eval(predicts, eval_data_y)

    def predict(self, eval_data_X):
        return self.__predict(eval_data_X)
