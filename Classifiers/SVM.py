# coding=utf-8
import BaseModel
from Preprocesser import Preprocess
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import sklearn.metrics as metrics
from sklearn.feature_extraction.text import HashingVectorizer
from Vectorizer import BOW
import numpy
import jieba


class SVM(BaseModel.BaseModel):
    ##params
  
    def __init__(self, all_data, eval_X, C, kernel):
        BaseModel.BaseModel.__init__(self, all_data)
        self.__eval_X = eval_X
        self.__eval_X_vec = []
        self._svm_clf = None
        self.common_tokenizer = lambda x: jieba.cut(x)

        ##parmas
        self.__C = C
        self.__kernel = kernel

    def __train_n(self, train_X, train_y, vec=1):
        model = SVC(C=self.__C, kernel=self.__kernel)
        #########
        ## error: 数据没有对齐! 关键不知道LDA表示文档应该采用哪种形式?
        #########
        self._svm_clf = model.fit(train_X, train_y)


    def __vectorize1(self, X_train, X_test):
        X_train_new = []
        X_test_new = []
        for x in X_train:
            X_train_new.append(' '.join(x))
        for x in X_test:
            X_test_new.append(' '.join(x))

        vector = HashingVectorizer(tokenizer=self.common_tokenizer, n_features=8000, non_negative=True)
        x_train_vec = vector.fit_transform(X_train_new)
        x_test_vec = vector.fit_transform(X_test_new)
        print ""
        print 'X_train_vec.shape {}, x_test_vec.shape {}'.format(x_train_vec.shape, x_test_vec.shape) 
        return x_train_vec, x_test_vec

    # def __vectorize2(self, X_train, X_test):
    #     '''
    #     :function 使用LDA进行向量化
    #     '''
    #     lda_model = LDA.LDA()
    #     X_train_vec = lda_model.vectorize(X_train)
    #     X_test_vec = lda_model.vectorize(X_test)
    #     return X_train_vec, X_test_vec


    def __trans_data(self, data, train=False):
        if train:
            train_X = []
            train_y = []
            for i_class, articles in data.items():
                for article in articles:
                    train_X.append(article)
                    train_y.append(i_class)
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
        for k in Preprocess.new_class_map2.keys():
            print k, Preprocess.new_class_map2[k]
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
        self.__train_n(train_X, train_y, vec=2)
        print 'train done'

    def predict(self, eval_X):
        return self.__predict(eval_X)

    def eval(self, predicts, truth):
        self.__eval(predicts, truth)