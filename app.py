from flask import Flask,render_template,request,redirect,url_for
import main as an
import numpy as np
import os

app = Flask(__name__)
nlp = an.nlp

def fileReader(types,fileName):
    temp = request.files[types]
    temp.save(fileName)
    text = an.cleaner(an.pdfReader(fileName))
    return text

def similarity(cv,jd):
    text = [cv,jd]
    cv = an.CountVectorizer()
    countMatrix = cv.fit_transform(text)
    matchPercentage = an.cosine_similarity(countMatrix)[0][1]*100
    print(f'The similarity between the resume and JD is {round(matchPercentage,2)}%')
    
    return matchPercentage

def keywordsDetector(cv,jd):
    matcher = an.PhraseMatcher(nlp.vocab)
    terms = an.keywords(jd,ratio=0.3).split('\n')
    patterns = [nlp.make_doc(t) for t in terms]
    matcher.add('Specs',patterns)
    doc = nlp(cv)
    matchKeywords =[]
    matches = matcher(doc)
    for match_id,start,end in matches:
        span = doc[start:end]
        matchKeywords.append(span.text)
    
    a = an.Counter(matchKeywords)
    return a,terms

def missKeywords(jdList,matchKeywords):
    return np.setdiff1d(jdList,matchKeywords)

@app.route('/')
def home():
    try:
        os.remove('JD.pdf')
        os.remove('tempCV.pdf')
    except:
        pass
    return render_template('home.html')

@app.route('/analysis',methods=['POST','GET'])
def analysis():
    cvsText = fileReader('cv','tempCV.pdf')
    jobsText = fileReader('jd','JD.pdf')
    
    percentage = similarity(cvsText,jobsText)
    matchedKeys,compList = keywordsDetector(cvsText,jobsText)
    matchedKeys = sorted(matchedKeys.items(),key=lambda x:x[1],reverse=True)
    matchedKeys = {k:v for k,v in matchedKeys}
    matchedKeys = [*matchedKeys]
    matchedKeysFinal = matchedKeys[:5] if len(matchedKeys)>5 else matchedKeys
    print(matchedKeysFinal)
    
    missedWords = missKeywords(compList,matchedKeys)
    print(f'the missing words are {missedWords}')
    
    return render_template('result.html',
                           percentage = round(percentage),
                           matchKeywords=matchedKeysFinal,
                           missedKeywords =missedWords[:5])

if __name__ == '__main__':
    app.run(debug=True)