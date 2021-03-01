import PyPDF2
import os
from collections import Counter
import en_core_web_sm
from spacy.matcher import PhraseMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import matplotlib.pyplot as plt
import numpy as np

nlp = en_core_web_sm.load()

def pdfReader(filePath):
    fileReader = PyPDF2.PdfFileReader(open(filePath,'rb'))
    # print(f'The number of pages in the {filePath} is {fileReader.getNumPages()}')
    count = 0
    text = []
    while count < fileReader.getNumPages():    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()
        text.append(t)
    return text

def cleaner(string):
    text = ''
    for s in string:
        text += s.lower().replace('\\n','').replace('!','').replace('|','')
    text = re.sub(' +', ' ',text)
    return text

def ploter(dictionary):
    lst = sorted(dictionary.items(),key=lambda kv: kv[1],reverse=True)
    print(lst)
    x,y = zip(*lst)

    plt.bar(x,y)
    plt.show()


if __name__ =='__main__':
    cvs = r'Muhammad_Saad_resume - CA.pdf'
    job = r'DeveloperJobDescription.pdf'

    ## reading the files
    cvsText = cleaner(pdfReader(cvs))
    jobText = cleaner(pdfReader(job))

    ## displaying the result
    # print(cvsText)
    # print('-'*100)
    # print(jobText)

    overallText = [cvsText,jobText]
    cv = CountVectorizer()
    countMatrix = cv.fit_transform(overallText)
    matchPercentage = cosine_similarity(countMatrix)[0][1]*100
    print(f'The similarity between the resume and JD is {round(matchPercentage,2)}%')

    matcher = PhraseMatcher(nlp.vocab)
    terms = keywords(jobText,ratio=0.3).split('\n')
    patterns = [nlp.make_doc(t) for t in terms]
    matcher.add('Specs',patterns)
    doc = nlp(cvsText)
    matchKeywords =[]
    matches = matcher(doc)
    for match_id,start,end in matches:
        span = doc[start:end]
        matchKeywords.append(span.text)
    
    a = Counter(matchKeywords)
    # ploter(a)

    
    main_list = np.setdiff1d(terms,matchKeywords)
    print(main_list)
    print(len(main_list))
    print(len(terms))

