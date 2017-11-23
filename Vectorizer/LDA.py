# coding = 'utf-8'

'''
LDA model for text classification task.
@author: shaw 2017-11-13
'''


from Preprocesser import Preprocess
from gensim.models import LdaMulticore, TfidfModel
from gensim.corpora import Dictionary
from gensim import corpora, models, similarities

class MyCorpus(object):
    def __iter__(self):
        for line in data:
            yield dictionary.doc2bow(line)

def get_train():
    for k, v in all_articles.items():
        for a in v:
            yield a

all_articles = Preprocess.process_all_articles('data/fenghuangnews/', 10)
data = [x for x in get_train()]
dictionary = Dictionary(data)
dictionary.save('lda.dict')
corpus = MyCorpus()
corpora.MmCorpus.serialize('lda.mm', corpus)


class LDA:
    def __init__(self):
        pass

    def train(self):
        tfidf = TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        lda = LdaMulticore(corpus=corpus_tfidf, id2word=dictionary, num_topics=100)
        lda.save('lda.model')

    def vectorize(self, data):
        dictionary = corpora.Dictionary.load('Vectorizer/lda.dict')
        data_bow = [dictionary.doc2bow(text) for text in data]
        lda_model = models.LdaMulticore.load('Vectorizer/lda.model')
        data_vec = [lda_model[t] for t in data_bow]
        return data_vec


if __name__ == '__main__':
    lda = LDA()
    # lda.train()
    # vec = lda.vectorize(data)
