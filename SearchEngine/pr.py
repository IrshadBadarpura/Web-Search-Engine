import pickle, os

def loadPickle(name):
	with open(name, 'rb') as f:
		return pickle.load(f)

def inlinkFunc(tfidf,crawled):
    inlink ={}

    for url in tfidf:
        inlink[url] = []
        for crawlUrl in crawled:
            if url in crawled[crawlUrl][2]:
                inlink[url].append(crawled[crawlUrl][0]) 

    return inlink

def pqitoj(term, i, j, tfidf):
    s = 0
    for doc in webCrawled[i][2]:
        if doc in tfidf and term in tfidf[doc]:
            s += tfidf[doc][term]

    return (tfidf[j][term] if term in tfidf[j] else 0)/s

def queryDependentPageRank(tfidf, crawled, inlink):
    alpha = 0.85
    queryDependentPageRank = {}

    for url in tfidf:
        queryDependentPageRank[url] = {}
        for token in tfidf[url]:
            queryDependentPageRank[url][token] = 1/len(tfidf[url])
    
    iteration = 0

    while( iteration < 10) :
        corr = 0
        
        for url in tfidf:
            corr += 1
            
            for token in tfidf[url]:
               
                s = 0
                for i in inlink[url]:
                   
                    # if token in queryDependentPageRank[i]:
                    #     s += queryDependentPageRank[i][url] * pqitoj(token, i, url, tfidf)
                    #     print("Here")
                    # else :
                    #     s += 0
                    s += (queryDependentPageRank[i][token] if token in queryDependentPageRank[i] else 0) * pqitoj(token, i, url, tfidf)
                    # print(s)
                prQuery = tfidf[url][token]/ sum(tfidf[i][token] if token in tfidf[i] else 0 for i in tfidf)  
                queryDependentPageRank[url][token] = (1 - alpha) * prQuery + (alpha * s)
        iteration += 1
    return queryDependentPageRank

if __name__ == "__main__":

    webCrawled = loadPickle("webCrawled_pages.pkl")
    # print(webCrawled)
    tfidf = loadPickle("tf-idf.pkl")
    
    if os.path.exists('inlink.pkl'):
        inlink = loadPickle("inlink.pkl")
    
    else:
        inlink = inlinkFunc(tfidf,webCrawled)
        with open('inlink.pkl', 'wb') as f:
            pickle.dump(inlink, f)

    qr = queryDependentPageRank(tfidf, webCrawled, inlink)
    # print(qr)
    with open('queryDependentPageRank.pkl', 'wb') as f:
        pickle.dump(qr, f)
    
    qr = loadPickle('queryDependentPageRank.pkl')
    
    

