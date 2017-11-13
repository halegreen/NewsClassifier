# coding = 'utf-8'

'''
LDA model for text classification task.
@author: shaw 2017-11-03
'''


from Preprocesser import Preprocess
from gensim.models import LdaModel
from gensim.corpora import Dictionary


class LDA:

    def __init__(self):
        self.all_articles = Preprocess.process_all_articles('data/fenghuangnews/', 100)

    def get_train(self):
        for k, v in self.all_articles.items():
            for a in v:
                yield a

    def vectorize(self):
        train = [x for x in self.get_train()]
        dictionary = Dictionary(train)
        corpus = [dictionary.doc2bow(text) for text in train]
        lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
