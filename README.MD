IR Project: Web Search Engine
Name: Irshad B. Badarpura
UIN: 653954954

#Files/Folders:
##The zip file has the following structure:
-SearchEngine
	-images
	-report
		-report
	-search.png
	-index.py
	-tf-idf.py
	-inlink.py
	-pr.py
	-userInterface.py [To start the interface/ search engine please run this file]
	-webCrawled_pages.pkl
	-vocab.pkl
	-totalWords.pkl
	-tf-idf.pkl
	-inlink.pkl
	-queryDependentPageRank.pkl
	-crawler.pkl
	-README [This file contains the instructions to run the code and get output from the code]

#System Requirements:
The system should have the following to execute the IRHW2F.py file:
-Pycharm Community Edition 2019.3.2 / Visual Studio Code
-python 3.6+
-please make sure to import the following libraries before executing the userInterface.py file
	-nltk
	-pickle
	-tkinter
	-PIL, Image, ImageTK
	-os
	-math, re, string

#How to implement the code:
-If using PyCharm, open the unzipped folder in PyCharm and then open userInterface.py.Then, press shift+crtl+10 or right click and then press run to run the code. A new interface window opens.This is the search engine window. Put any query and select the method of search and a list box displays the top pages.
-If using Visual Studio Code,open the unziped folder in Visual Studio Code and then open userInterface.py.Then, in the terminal type the following command
	-python IRHW2F.py
A new interface window opens.This is the search engine window. Put any query and select the method of search and a list box displays the top pages.

--Note: Please only run the userInterface.py file. There is no need to run other files.
Also, if you want to run from sratch, first delete all the existing pickle files then run in the following files in the following order:
- index.py
- tf-idf.py
- inlink.py
- pr.py
- userInterface.py


