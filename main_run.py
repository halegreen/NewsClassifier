#encoding=utf-8
from Classifiers import NaiveBayes
from Classifiers import SVM, RandomForest
from Preprocesser.DataIO import DataIO
from Vectorizer.BOW import BOW
import time
import codecs
import gc
import dill as pickle

## data_szie:取的数据量; mode:数据分割的方式
## hyper parameters
global_data_size = 1000
feat_dim = 600


#1.split data
t1_s = time.time()
dataio = DataIO('', global_data_size)
print '====== Getting data ... ======'
all_articles = dataio.get_all_data()
train_data = dataio.get_train_data()
eval_data_X = dataio.get_eval_data_X()
eval_data_y = dataio.get_eval_data_y()
del dataio
gc.collect()
trian_num = 0
for k in train_data.keys():
    trian_num += len(train_data[k])
print 'data for train: %s, data for eval: %s' % (trian_num, len(eval_data_y))
t1_e = time.time()
print 'all_data loaded done, time comsumed %s ' % (t1_e - t1_s)


# get dict
print '==== Loading data..===='
all_data, article_num = DataIO.get_final_data(data_size=global_data_size)
print '===== Create BOW...====='
feat = feat_dim  ##字典的纬度等于 feaet * class_num
bow = BOW(feature_word_num=feat, all_data=all_data)
del all_data
gc.collect()
with open('data/bow.pkl', 'wb') as f:
	pickle.dump(bow, f, -1)
del bow
gc.collect()

##2.
print '====== Loading NaiveBayes Model... ====='
nb_clf = NaiveBayes.NaiveBayes(all_articles)
print '====== Trainnig NaiveBayes Model... ====='
nb_clf.train(train_data)
print '====== Predicting...======'
predicts = nb_clf.predict(eval_data_X)
print '====== Evalling Model... ======'
mat_matrix = nb_clf.eval(predicts, eval_data_y)

#3.
print '====== Loading SVM Model... ======'
svm_clf = SVM.SVM(all_articles, eval_data_X, C=2.0, kernel='linear')
print '====== Training SVM Model...======'
svm_clf.train(train_data)
print '====== Predicting SVM...======'
predicts = svm_clf.predict(eval_data_X)
print '====== Evalling SVM...======'
svm_clf.eval(predicts, eval_data_y)

#4.
print '====== Loading RF Model... ======'
rf_clf = RandomForest.RandomForest(all_articles, eval_data_X, depth=8)
print '====== Training RF Model...======'
rf_clf.train(train_data)
print '====== Predicting RF...======'
predicts = rf_clf.predict(eval_data_X)
print '====== Evalling RF...======'
rf_clf.eval(predicts, eval_data_y)

del all_articles, train_data, eval_data_X, eval_data_y
gc.collect()

