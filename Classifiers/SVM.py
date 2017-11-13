# coding=utf-8
import BaseModel
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import sklearn.metrics as metrics
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class SVM(BaseModel.BaseModel):

    def __init__(self, all_data, eval_X):
        BaseModel.BaseModel.__init__(self, all_data)
        self.__eval_X = eval_X
        self.__eval_X_vec = []
        self._svm_clf = None

    def __train_n(self, train_X, train_y):
        train_X = pd.DataFrame(train_X)
        train_y = pd.DataFrame()
        model = SVC(C=1.0, kernel='linear')
        self._svm_clf = model.fit(train_X, train_y)


    def __vectorize1(self, X_train, X_test):
        count_vect = CountVectorizer(decode_error='ignore')
        X_train_counts = count_vect.fit_transform(X_train)
        X_test_counts = count_vect.fit_transform(X_test)
        print 'X_train_counts.shape %s' % X_train_counts.shape
        tf_transfomer = TfidfTransformer(use_idf=True).fit(X_train_counts)
        X_train_tf = tf_transfomer.transform(X_train_counts)
        X_test_tf = tf_transfomer.transform(X_test_counts)
        print 'X_train_tf.shap %s' % X_train_tf.shape
        return X_train_tf, X_test_tf

    def __vectorize2(self, X_train, X_test):
        '''
        :function 使用LDA进行向量化
        '''


    def __trans_data(self, data, train=False):
        if train:
            train_X = []
            train_y = []
            n_data = pd.DataFrame(data)
            for x, y in data.items():
                train_X.append(x)
                train_y.append(y)
            return train_X, train_y
        else:
            n_data = pd.DataFrame(data)
            return n_data

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


    def __predict(self, _):
        ## using self.__eval_X_vec
        predicts = self._svm_clf.predict(self.__eval_X_vec)
        return predicts

    def train(self, train_data):
        train_X, train_y = self.__trans_data(train_data, train=True)
        train_X, self.__eval_X_vec = self.__vectorize1(train_X, self.__eval_X)
        self.__train_n(train_X, train_y)

    def predict(self, eval_X):
        return self.predict(eval_X)

    def eval(self, predicts, truth):
        self.__eval(predicts, truth)