import flask 
from flask import render_template
from flask import request
from flask.json import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

import json
import pandas as pd
import time
import numpy as np
import itertools
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import flask
tweets_data = []
x = []
y = []
vectorizer = CountVectorizer(stop_words='english')

def retrieveTweet(data_url):

    tweets_data_path = data_url
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue 

def retrieveProcessedData(Pdata_url):
    sent = pd.read_excel(Pdata_url)
    for i in range(len(tweets_data)):
        if tweets_data[i]['id']==sent['id'][i]:
            x.append(tweets_data[i]['text'])
            y.append(sent['sentiment'][i])

     
retrieveTweet('E:\#STUDY\Coding v1\euphoria\data/tweetdata.txt')  
retrieveProcessedData('E:\#STUDY\Coding v1\euphoria\processed_data/output.xlsx') 
from sklearn import tree
train_featurestree = vectorizer.fit_transform(x)
actual1 = y
test_features1 = vectorizer.transform(x)
dtree = tree.DecisionTreeClassifier()
dtree = dtree.fit(train_featurestree, [int(r) for r in y])
    
def datreeINPUT(inputtweet):
    inputdtree= vectorizer.transform([inputtweet])
    predictt = dtree.predict(inputdtree)
    if(predictt == 0 or predictt == -1):
        return predictt
    else:
        return (predictt-1)

@app.route('/')
def home():
    print("We have a visitor!")
    return render_template('index.html')

@app.route('/depression', methods=['GET' , 'POST'])
def depression():
    if(request.method=='POST'):
        print()
        print("post req received :",request.json)
        answer=datreeINPUT(request.json)
        answer=str(answer[0])
        print("answer ",answer)
        return jsonify(answer)
    elif(request.method=='GET'):
        print("get req received")
        print(request)
        return "Hello"

app.run(debug=True)