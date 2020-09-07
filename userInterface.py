import pickle
import os 

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize

import math,re

import tkinter as tk
from PIL import Image, ImageTk

inverted = {}
cosine = {}
ranking_docs = []


def loadPickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def inverted_index(url,tokens):

    global inverted

    for items in set(tokens):
        if items in inverted:
            docs_exist = inverted[items][1]
            docs_exist[url] = tokens.count(items)
            inverted[items] = [inverted[items][0]+1,docs_exist]
       
        else:
            inverted[items] = [1,{url:tokens.count(items)}]

def tf_idf(data1,data2):
    tf_word = []
    N = len(webCrawled)
    weight = 0
    for word in data2:
        if word in inverted:
            idf = math.log(N/inverted[word][0],2)
            dictemp = inverted[word][1]
            tf = dictemp[data1]/result[data1]
            tfidf = tf*idf
            tf_word.append(tfidf)
   
    for tidf in tf_word:
        weight += (tidf * tidf)
       
    doclen = math.sqrt(weight)
    return doclen 

def tokenize(data):
    tokenizing = str.maketrans(dict.fromkeys(string.punctuation))
    cleaning_data = data.translate(tokenizing)
    remove_num = re.sub('[0-9]+','',cleaning_data)
    tokenized = word_tokenize(remove_num)
    tokenized = [element.lower() for element in tokenized]
    no_integers = [x for x in tokenized if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    return no_integers

def port_stem(data):
    portstem = PorterStemmer()
    ps = []
    for words in data:
        ps.append(portstem.stem(words))
    return ps

def stop_words(data):
    filtered_word_list = data[:]
    for word in data:
        if word in stopwords.words('english'):
            filtered_word_list.remove(word)
    return filtered_word_list

def preprocessquery(query):
    removed_tokens_query = tokenize(query)
    removed_stem_query = port_stem(removed_tokens_query)
    removed_stop_words_query = stop_words(removed_stem_query)
    return (removed_stop_words_query)

def qtf_idf(query):
    unique=list(set(query))
    qlen=[]
    global q_tf
    for q in unique:
        if q in query:
            qtf=query.count(q)
            qlen.append(qtf)
            q_tf.update({q:qtf})
    qweight=0
    for ele in qlen:
        qweight+=(ele*ele)
    length=math.sqrt(qweight)
    return length

def cosine_simi(queryProcessed,querylength,length_dict):
    global cosine
    global ranking_docs
    for word in queryProcessed:
        try:
            for files in inverted[word][1]:
                if files in cosine:
                    cosine[files] += (inverted[word][1][files]/result[files])*math.log((len(webCrawled)/inverted[word][0]),2)
                else:
                    cosine[files] = (inverted[word][1][files]/result[files])*math.log((len(webCrawled)/inverted[word][0]),2)
        except:
            print(word+" not in the documents")

    ranking_sorted_docs = []
    for files in cosine:
        cosine[files] = cosine[files]/( length_dict[files] * querylength)
   
    rank_sort = sorted(cosine.items(), key = lambda k: k[1], reverse = True)
    [ ranking_sorted_docs.append(k) for k,v in rank_sort]
    ranking_docs.append(ranking_sorted_docs)

    return ranking_sorted_docs

def score(pageranks, query):
    prob_query = {}
    ranks = {}
    for word in query:
        prob_query[word] = 1/len(query)
    for doc in pageranks:
        ranks[doc] = sum(prob_query[word]*pageranks[doc][word] if word in pageranks[doc] else 0 for word in query)

    ranking_sorted_docs = []
    rank_sort = sorted(ranks.items(), key = lambda k: k[1], reverse = True)
    [ ranking_sorted_docs.append(k) for k,v in rank_sort]
    
    return ranking_sorted_docs

def UI():
    
    root =tk.Tk()
    root.geometry("700x450")

    def userText(event):
        entry.delete(0,"end")
        usercheck=True
        print(usercheck)

    usercheck = False
    print(usercheck)

    def getText ():
        text_box.place(relx=0.2,rely=0.35)
        query = entry.get()
        queryProcessed = preprocessquery(query)
        querylength = qtf_idf(queryProcessed)
        ranked = cosine_simi(queryProcessed,querylength,length_dict)

        # text_box.delete(tk.ACTIVE)
        text_box.delete(0,tk.END)

        text_box.insert(1,ranked[0])
        text_box.insert(2,"\n"+ranked[1])
        text_box.insert(3,"\n"+ranked[2])
        text_box.insert(4,"\n"+ranked[3])
        text_box.insert(5,"\n"+ranked[4])
        text_box.insert(6,"\n"+ranked[5])
        text_box.insert(7,"\n"+ranked[6])
        text_box.insert(8,"\n"+ranked[7])
        text_box.insert(9,"\n"+ranked[8])
        text_box.insert(10,"\n"+ranked[9])

        def back():
            text_box.delete(0,tk.END)
            # text_box.delete(tk.ACTIVE)
            
            buttonBack.destroy()
            buttonMore.destroy()

        buttonBack = tk.Button(text="Back",command=back)
        buttonBack.place(relx=0.72,rely=0.9)

        def extra():
            text_box.delete(0,tk.END)
            buttonBack.destroy()

            newWindow = tk.Tk()
            newWindow.geometry("600x500")
            newWindow.title("More Results")
            buttonMore.destroy()
            
            newText = tk.Listbox(newWindow,height=25,width = 80)
            newText.place(relx=0.1,rely=0.1)

            query = entry.get()
            queryProcessed = preprocessquery(query)
            querylength = qtf_idf(queryProcessed)
            ranked = cosine_simi(queryProcessed,querylength,length_dict)

            newText.insert(1,ranked[0])
            newText.insert(2,"\n"+ranked[1])
            newText.insert(3,"\n"+ranked[2])
            newText.insert(4,"\n"+ranked[3])
            newText.insert(5,"\n"+ranked[4])
            newText.insert(6,"\n"+ranked[5])
            newText.insert(7,"\n"+ranked[6])
            newText.insert(8,"\n"+ranked[7])
            newText.insert(9,"\n"+ranked[8])
            newText.insert(10,"\n"+ranked[9])
            newText.insert(11,"\n"+ranked[10])
            newText.insert(12,"\n"+ranked[11])
            newText.insert(13,"\n"+ranked[12])
            newText.insert(14,"\n"+ranked[13])
            newText.insert(15,"\n"+ranked[14])
            newText.insert(16,"\n"+ranked[15])
            newText.insert(17,"\n"+ranked[16])
            newText.insert(18,"\n"+ranked[17])
            newText.insert(19,"\n"+ranked[18])
            newText.insert(20,"\n"+ranked[19])
            
            def exit():
                def windowClose():
                    root.destroy()
                buttonExit = tk.Button(root,text="Exit",command=windowClose)
                buttonExit.place(relx=0.9,rely=0.9)
            def close():
                newWindow.destroy()
                exit()
            buttonClose = tk.Button(newWindow,text="Close",command=close)
            buttonClose.place(relx=0.8,rely=0.94)
            newWindow.mainloop()
        
        buttonMore = tk.Button(text="Show More Results",command=extra)
        buttonMore.place(relx=0.2,rely=0.9)

    def getPR ():
        text_box.place(relx=0.2,rely=0.35)
        query = entry.get()
        pagerank = loadPickle('queryDependentPageRank.pkl')
        queryProcessed = preprocessquery(query)
        pageRankCalc = score(pagerank,queryProcessed)
        # text_box.delete(tk.ACTIVE)
        text_box.delete(0,tk.END)
        

        text_box.insert(1,pageRankCalc[0])
        text_box.insert(2,"\n"+pageRankCalc[1])
        text_box.insert(3,"\n"+pageRankCalc[2])
        text_box.insert(4,"\n"+pageRankCalc[3])
        text_box.insert(5,"\n"+pageRankCalc[4])
        text_box.insert(6,"\n"+pageRankCalc[5])
        text_box.insert(7,"\n"+pageRankCalc[6])
        text_box.insert(8,"\n"+pageRankCalc[7])
        text_box.insert(9,"\n"+pageRankCalc[8])
        text_box.insert(10,"\n"+pageRankCalc[9])
        

        def back():
            # text_box.delete(tk.ACTIVE)
            text_box.delete(0,tk.END)
            buttonBack.destroy()
            buttonMore.destroy()

        buttonBack = tk.Button(text="Back",command=back)
        buttonBack.place(relx=0.72,rely=0.9)
        
        def extra():
            text_box.delete(0,tk.END)
            buttonBack.destroy()
            newWindow = tk.Tk()
            newWindow.geometry("600x500")
            newWindow.title("More Results")
            buttonMore.destroy()
            
            newText = tk.Listbox(newWindow,height=25,width = 80)
            newText.place(relx=0.1,rely=0.1)

            query = entry.get()
            pagerank = loadPickle('queryDependentPageRank.pkl')
            queryProcessed = preprocessquery(query)
            pageRankCalc = score(pagerank,queryProcessed)
            
            newText.insert(1,pageRankCalc[0])
            newText.insert(2,"\n"+pageRankCalc[1])
            newText.insert(3,"\n"+pageRankCalc[2])
            newText.insert(4,"\n"+pageRankCalc[3])
            newText.insert(5,"\n"+pageRankCalc[4])
            newText.insert(6,"\n"+pageRankCalc[5])
            newText.insert(7,"\n"+pageRankCalc[6])
            newText.insert(8,"\n"+pageRankCalc[7])
            newText.insert(9,"\n"+pageRankCalc[8])
            newText.insert(10,"\n"+pageRankCalc[9])
            newText.insert(11,"\n"+pageRankCalc[10])
            newText.insert(12,"\n"+pageRankCalc[11])
            newText.insert(13,"\n"+pageRankCalc[12])
            newText.insert(14,"\n"+pageRankCalc[13])
            newText.insert(15,"\n"+pageRankCalc[14])
            newText.insert(16,"\n"+pageRankCalc[15])
            newText.insert(17,"\n"+pageRankCalc[16])
            newText.insert(18,"\n"+pageRankCalc[17])
            newText.insert(19,"\n"+pageRankCalc[18])
            newText.insert(20,"\n"+pageRankCalc[19])

            def exit():
                def windowClose():
                    root.destroy()
                buttonExit = tk.Button(root,text="Exit",command=windowClose)
                buttonExit.place(relx=0.9,rely=0.9)
            def close():
                newWindow.destroy()
                exit()
            buttonClose = tk.Button(newWindow,text="Close",command=close)
            buttonClose.place(relx=0.85,rely=0.93)
            newWindow.mainloop()
        

        buttonMore = tk.Button(text="Show More Results",command=extra)
        buttonMore.place(relx=0.2,rely=0.9)
        
    root.title("UIC Search Engine")
    U = tk.Label(root,text="U",font=(None,40),fg="navy")
    U.place(relx = 0.45, rely = 0.1, anchor = 'center') 

    I = tk.Label(root,text="I",font=(None,40),fg="red2")
    I.place(relx = 0.5, rely = 0.1, anchor = 'center')

    C = tk.Label(root,text="C",font=(None,40),fg="navy")
    C.place(relx = 0.55, rely = 0.1, anchor = 'center') 

    entry = tk.Entry(width=50)
    entry.insert(0,'Enter your query')
    entry.place(relx=0.5,rely = 0.2, anchor = 'center')
    entry.bind("<Button>",userText)

    searchImg = Image.open(r'./search.png')
    useSearch = ImageTk.PhotoImage(searchImg)
    searchLabel = tk.Label(entry,image=useSearch,bg="white")
    searchLabel.place(relx=0.94)

    button1 = tk.Button(text="Tf-idf Search",command=getText)
    button1.place(relx=0.37,rely=0.25)

    button2 = tk.Button(text="PageRank Search",command=getPR)
    button2.place(relx=0.5,rely=0.25)

    text_box = tk.Listbox(root,height=15,width = 70)

    root.mainloop()

if __name__== "__main__":

    webCrawled = loadPickle('webCrawled_pages.pkl')
    
    # print(pagerank)
    dictionaryTokens = {}
    result = {}
    length_dict = {}
    q_tf = {}

    for url in webCrawled.keys():
        x,y = url, webCrawled[url][1]
        res = max(set(y),key = y.count)
        result.update({x:(y.count(res))})
        dictionaryTokens.update({x:y})
        inverted_index(x,y)
    
    for url,tokens in dictionaryTokens.items():
        z =set(tokens)
        length = tf_idf(url,list(z))
        length_dict.update({url:length})

    UI()

