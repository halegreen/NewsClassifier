# coding=utf-8

import BaseModel
from Preprocesser import Preprocess
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer



class RandomForest(BaseModel.BaseModel):

    def __init__(self):
        super(RandomForest, self).__init()

    def __train(self, train_data):
        X_train = []
        Y_train = []
        X_train_vec = self.__vectorize(X_train)
        pass


    def __vectorize(self, X_train):
        count_vect = CountVectorizer(decode_error='ignore')
        X_train_counts = count_vect.fit_transform(X_train)
        print X_train_counts.shape

        tf_transfomer = TfidfTransformer(use_idf=True).fit(X_train_counts)
        X_train_tf = tf_transfomer.transform(X_train_counts)
        print X_train_tf.shape

        return X_train_tf



    def __eval(self, predicts, eval_data_y):
        pass

    def __predict(self, test_data):
        pass

    def train(self, train_data):
        self.__train(train_data)

    def predict(self, test_data):
        self.predict(test_data)