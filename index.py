import re, os, requests

import pickle

from collections import deque

from bs4 import BeautifulSoup

from urllib.parse import urlparse
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize

pageIndex = 0

def tokenize(data):
    tokenizing = str.maketrans(dict.fromkeys(string.punctuation))
    cleaning_data = data.translate(tokenizing)
    remove_num = re.sub('[0-9]+','',cleaning_data)
    tokenized = word_tokenize(remove_num)
    tokenized = [element.lower() for element in tokenized]
    no_integers = [x for x in tokenized if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    return no_integers

def stop_words(tokens):
    filtered_word_list = tokens[:]
    for word in tokens:
        if word in stopwords.words('english'):
            filtered_word_list.remove(word)
    return filtered_word_list  

def port_stem(stop):
    portstem = PorterStemmer()
    ps = []
    for words in stop:
        ps.append(portstem.stem(words))
    return ps

def length_clean(data):
    length_removed = []
    for words in data:
        if len(words) >2 :
            length_removed.append(words)
    return length_removed

def openPickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def savePickle(filename,obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def getData (visited,vocab) :
    # base = []
    i = 0
    for url in visited:
        try:
            response = urlopen("http://"+url)
            i += 1
        except Exception as e:
            print(e,url)
            continue
        # base.append(urlparse("http://"+url).netloc)
        base = [urlparse(u).netloc for u in url]    
        soup = BeautifulSoup(response,'html.parser')
        try:
            textTitle = soup.find('title').text
        except:
            continue
        textP = soup.find_all('p')
        textPContent = [p.text for p in textP]
        textSpan = soup.find_all('span')
        textSpanContent = [span.text for span in textSpan]
        textH1 = soup.find_all('h1')
        textH1Content = [h.text for h in textH1]
        textH2 = soup.find_all('h2')
        textH2Content = [h.text for h in textH2]
        textH3 = soup.find_all('h3')
        textH3Content = [h.text for h in textH3]
        textH4 = soup.find_all('h4')
        textH4Content = [h.text for h in textH4]
        textH5 = soup.find_all('h5')
        textH5Content = [h.text for h in textH5]
        textH6 = soup.find_all('h6')
        textH6Content = [h.text for h in textH6]
        textDiv = soup.find_all('div')
        textDivContent = [div.text for div in textDiv]
        
        data = textTitle + ' '.join(textPContent) + ' '.join(textSpanContent) + ' '.join(textH1Content) + ' '.join(textH2Content) + ' '.join(textH3Content) + ' '.join(textH4Content) + ' '.join(textH5Content) + ' '.join(textH6Content) + ' '.join(textDivContent)

        crawler[url] = {'data':data} 
        
        data = re.sub('\n',' ',data)

        tokens = tokenize(data)
        stopWordRemoved = stop_words(tokens)
        stemmed = port_stem(stopWordRemoved)
        stopWordRemoved2 = stop_words(stemmed)
        removedLength = length_clean(stopWordRemoved2)

        totalWords[url] = {}
        vocabulary = True
        for token in removedLength:
            if token in totalWords[url].keys():
                totalWords[url][token] += 1
            else:
                totalWords[url][token] = 1
            
            if token not in vocab:
                vocab[token] = 1
            elif vocabulary:
                vocab[token] += 1
                vocabulary = False
        
        links = [urljoin(url, l.get('href')) for l in soup.findAll('a')]
        links = [l.rstrip("/") for l in links if urlparse(l).netloc in base]
        finalData = (url,removedLength,list(set(links)))
        if finalData != (-1) :
            webCrawled[url] = finalData
    print(i)
    return webCrawled

def start():
    global pageIndex
    while(len(urlQueue) != 0):
            try:
                url = urlQueue.pop(0)
                if url not in urlVisited:
                    urlVisited.add(url)

                req = requests.get("http://"+url)

                if(req.status_code == 200):
                    
                    urlLinks[pageIndex] = url
                
                    soup = BeautifulSoup(req.text, 'html.parser')
                    aTags = soup.find_all('a')
                    for aTag in aTags:
                        try:
                            if(re.search('.+?uic.edu',aTag["href"]) != None):
                                if not any(word in aTag["href"] for word in outDomain):
                                    parse = urlparse(aTag["href"])
                                    ls = (parse.netloc + parse.path).lstrip("www.")
                                    new_href = ls.rstrip("/")
                                    if(inDomain in aTag["href"]):
                                        if not(new_href in urlVisited and new_href in urlLinks.values()):
                                            urlQueue.append(new_href)
                                            
                        
                        except:
                            continue
                    
                    pageIndex += 1
                    print(pageIndex)
                    if( stopAt < pageIndex):
                        print(pageIndex)
                        break
            except:
                print("Connection failed for ", url)
                continue
    return urlVisited

if __name__ == "__main__":

    crawler = {}
    path = os.getcwd()

    if not (os.path.isfile('webCrawled_pages.pkl') and os.path.isfile('totalWords.pkl') and os.path.isfile('vocab.pkl')):

        urlQueue = []
        urlLinks = {}
        totalWords = {}
        vocab = {}
        webCrawled = {}
        urlVisited = set()
        urlStart = "https://www.cs.uic.edu/"
        stopAt = 3500

        inDomain = "uic.edu"
        outDomain = ['.css', 'mailto:', '.js',
                                '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc',
                                '.JPG', '.mp4', '.svg','favicon', '.ico']

        parse = urlparse(urlStart)
        onlyDomain = ( parse.netloc).lstrip("www.")
        urlQueue.append(onlyDomain)
        
        visited = start()
        crawledData = getData(visited,vocab) 

        savePickle('webCrawled_pages.pkl',crawledData)
        savePickle('totalWords.pkl',totalWords)
        savePickle('vocab.pkl',vocab)  
        with open('crawler.pkl', 'wb') as f:
            pickle.dump(crawler,f)  

    else:
        webCrawledPickle = openPickle('webCrawled_pages.pkl')
        totalWordsPickle = openPickle('totalWords.pkl')
        vocabPicle = openPickle('vocab.pkl')
        crawlerPickle = openPickle('crawler.pkl')
        
        # print(webCrawledPickle)
        # print(len(totalWordsPickle['uic.edu']))
        # print(totalWordsPickle)
        # print(len(vocabPicle))
        # print(crawlerPickle)



        
            
                        
                    





    