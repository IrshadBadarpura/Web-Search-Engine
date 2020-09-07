import pickle

def loadPickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def inlinkFunc(tfidf,crawled):
    inlink ={}

    for url in tfidf:
        inlink[url] = []
        for crawlUrl in crawled:
            if url in crawled[crawlUrl][2]:
                # print(crawled[crawlUrl][0])
                inlink[url].append(crawled[crawlUrl][0]) 

    return inlink
if __name__ == "__main__":

    tfidf = loadPickle('tf-idf.pkl')
    webCrawled = loadPickle('webCrawled_pages.pkl')
    inlink = inlinkFunc(tfidf,webCrawled)

    with open('inlink.pkl', 'wb') as f:
        pickle.dump(inlink, f)