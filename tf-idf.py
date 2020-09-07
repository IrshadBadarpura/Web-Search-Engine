import pickle
import numpy as num
def calcTfIdf(totalWords, vocab):

    tfidf = {}
    lengthDoc = len(totalWords)
    for url in totalWords:
        tfidf[url] = {}
        # print(tfidf)
        for tokens in totalWords[url]:
            tf = totalWords[url][tokens] / (max(word for word in totalWords[url].values()))

            idf = num.log2(lengthDoc/vocab[tokens])
            
            tfidf[url][tokens] = tf * idf
    return tfidf
        
def loadPickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def savePickle(filename,obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

if __name__ == "__main__":

    totalWordsPickle = loadPickle('totalWords.pkl')
    # print(len(totalWordsPickle))
    vocabPickle = loadPickle('vocab.pkl')
    webCrawledPickle = loadPickle('webCrawled_pages.pkl')

    tf_idf = calcTfIdf(totalWordsPickle,vocabPickle)
    # print(tf_idf)

    savePickle('tf-idf.pkl',tf_idf)

    