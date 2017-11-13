#encoding=utf-8
from Classifiers import NaiveBayes
from Classifiers import SVM
import Preprocesser.DataIO
import time

outer_data_dir = 'data/fenghuangnews/'
## data_szie:取的数据量; mode:数据分割的方式
dataio = Preprocesser.DataIO.DataIO(outer_data_dir, data_size=10, mode='nb')

t1_s = time.time()
print '====== Getting data ... ======'
all_articles = dataio.get_all_data()
train_data = dataio.get_train_data()
eval_data_X = dataio.get_eval_data_X()
eval_data_y = dataio.get_eval_data_y()
trian_num = 0
for k in train_data.keys():
    trian_num += len(train_data[k])
print 'data for train: %s, data for eval: %s' % (trian_num, len(eval_data_y))
t1_e = time.time()
print 'all_data loaded done, time comsumed %s ' % (t1_e - t1_s)

# print '====== Loading NaiveBayes Model... ====='
# nb_clf = NaiveBayes.NaiveBayes(all_articles)
# print '====== Trainnig NaiveBayes Model... ====='
# nb_clf.train(train_data)
# print '====== Predicting...======'
# predicts = nb_clf.predict(eval_data_X)
# # for eval, pred in zip(eval_data_X, predicts):
# #     print ' '.join(eval),' ====> ', pred
# #     print ''
# print '====== Evalling Model... ======'
# mat_matrix = nb_clf.eval(predicts, eval_data_y)

print '====== Loading SVM Model... ======'
svm_clf = SVM.SVM(all_articles, eval_data_X)
print '====== Train SVM...======'
svm_clf.train(train_data)
print '====== Predicting SVM...======'
predicts = svm_clf.predict(eval_data_X)
print '====== Eval SVM...======'
svm_clf.eval(predicts, eval_data_y)