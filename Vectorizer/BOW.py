# coding = 'utf-8'

'''
Bag Of Words model for text classification task.
@author: shaw, 2017-10-26
'''


from Preprocesser import Preprocess, DataIO
import math
import numba


class BOW(object):

    def __init__(self, feature_word_num, all_data):
        # print 'BOW init'
        self.all_articles = all_data
        self.all_article_feat = []
        self.article_num = 0
        self.class_num = len(self.all_articles.keys())
        ## num of the most relative between the word and the class, can be tuned !!!
        self.feature_word_num = feature_word_num
        self.all_features = set()
        self.vec_article = []

        self.main()


    def choose_feature(self, article, all_pages, article_idx):
        tmp_dict = {}
        for word in article:
            if word in tmp_dict:
                continue
            else:
                tmp_dict[word] = self.getTF_IDF(word, all_pages, article_idx)
        return tmp_dict


    def getTF_IDF(self, word, all_pages, article_idx):
        # print 'word %s , tf: %.6f, idf: %.6f ' % (word, self.getTF(word, article_idx), self.getIDF(word))
        return self.getTF(word, all_pages, article_idx) * self.getIDF(all_pages, word)

    @numba.jit()
    def getTF(self, word, all_pages, article_idx):
        cnt = 0
        word_list = all_pages[article_idx]
        for w in word_list:
            if w == word:
                cnt += 1
                # print 'cnt %s' % cnt
        return float(cnt) / len(word_list)

    @numba.jit()
    def getIDF(self, all_pages, word):
        df = 0
        for article in all_pages:
            if word in article:
                df += 1
        if df == 0:
            df = 1
        return math.log(self.article_num / df)

    @numba.jit()
    def create_dict(self):
        article_word_dict = {}  ## word set for every class
        article_idx = 0
        all_pages = []
        for key in self.all_articles.keys():
            for v in self.all_articles[key]:
                all_pages.append(v)
        self.article_num = len(all_pages)
        print '====== All articles num: %s ===== ' % self.article_num

        for i_class, articles in self.all_articles.items():
            tmp_feat = set()
            for article in articles:
                article_feat = self.choose_feature(article, all_pages, article_idx)
                self.all_article_feat.append(article_feat)
                tmp_feat |= set(article_feat.keys())
                article_idx += 1
            article_word_dict[i_class] = tmp_feat  ## word set for every class

        return article_word_dict



    def reduce_dimension(self, word_dict):
        ## use chi-square test to reduce dimension of the article word dict
        self.all_features = self.chi_square_test(word_dict)
        self.all_articles = self.reduce_dim_again(word_dict)
        print '====== Feature dimension is : %s ======' % len(self.all_features)


    def reduce_dim_again(self, word_dict):
        '''
        :param word_dict:
        :return:
        '''
        pass


    @numba.jit()
    def chi_square_test(self, word_dict):
        ## for every word, cacculate the chi_square value with the class it belongs to.
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
            chi_value = ((A * D - B * C) * (A * D - B * C)) / ((A + B) * (C + D))
            return chi_value
        res = set()
        for i_class, words in word_dict.items():
            class_feat = {}
            for word in words:
                chi_value = get_chi(word, i_class)
                class_feat[word] = chi_value
            class_feat = sorted(class_feat.items(), key=lambda x: x[1], reverse=True)  ## sort chi_value
            tmp_list = [k[0] for k in class_feat]

            if self.feature_word_num != -1:
                tmp_list = tmp_list[0: self.feature_word_num]
            # print ' '.join(tmp_list)
            res |= set(tmp_list)
        return res


    @numba.jit()
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



    def main(self):
        print '====== Create dict... ======'
        word_dict = self.create_dict()
        print '====== Reduce dimension... ======'
        self.reduce_dimension(word_dict)
        # print '====== Vectorizing... ======'
        # self.vectorize()


if __name__ == '__main__':
    feat = -1 ## can be tuned
    bow = BOW(feature_word_num=feat)
    bow.main()
