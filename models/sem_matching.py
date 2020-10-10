#To train model from scratch, uncomment the following code
"""
import json
import pandas as pd
import numpy as np
import pickle
import re
import nltk
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
stopwords=set(stopwords.words('english'))
temp=[]
for line in open('News.txt','r'):    
    temp.append(json.loads(line))
pickle.dump(temp,open('structured_news.pkl','wb'))
temp=pickle.load(open('structured_news.pkl','rb'))
#Preprocessing
data=[]
for d in temp:
    x=d['content']
    x=re.sub(r"\(function[\s\S]+\(\)",' ',x)
    x=re.sub('[^a-zA-Z0-9]',' ',x)
    x=x.lower()
    x=x.split()
    x=[lemmatizer.lemmatize(word) for word in x if word not in stopwords]
    data.append(x[:500])
    
#Doc2Vec
tagged_data=[TaggedDocument(d,[i]) for i,d in enumerate(data)]
model = Doc2Vec( vector_size=300 ,min_count=2,epochs = 100)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
model.save('doc2vec_1.model')
mymodel=gensim.models.Doc2Vec.load('doc2vec_1.model')  
#Extracting Vectors
vectors=[]
for news in data:
    vectors.append(list(model.infer_vector(news)))
pickle.dump(vectors,open('vectors.pkl','wb'))
vectors = pickle.load(open('vectors.pkl','rb'))
#Clustering
# wcss=[]
# for i in range(1,25):
#     kmeans=KMeans(n_clusters=i,init='k-means++')
#     kmeans.fit(vectors)
#     wcss.append(kmeans.inertia_)
# plt.plot(range(1,25),wcss)
# plt.show()
#Testing
test='SRINAGAR: Two terrorists who were killed in an encounter on Saturday were found to be carrying coronavirus according to their test reports which came in on Sunday. This is the first instance of any terrorist testing positive for Covid-19 in Jammu and Kashmir.'
test=test.lower()
test=test.split()
test=[lemmatizer.lemmatize(word) for word in test if word not in stopwords]
mymodel.docvecs.most_similar(positive=[mymodel.infer_vector(test)],topn=5)
"""


import json
import nltk
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
stopwords=set(stopwords.words('english'))

THRESHOLD = 0.5

lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))
MYMODEL = None  
# vectors = pickle.load(open('vectors.pkl','rb'))
NEWS_DATA = None

def get_model():
    global MYMODEL
    if not MYMODEL:
        MYMODEL = gensim.models.Doc2Vec.load('doc2vec_1.model') 
    return MYMODEL

def get_news_data():
    global NEWS_DATA
    if not NEWS_DATA:
        NEWS_DATA = pickle.load(open('structured_news.pkl','rb'))
    return NEWS_DATA

def predict(news):
    mymodel = get_model()
    news_data = get_news_data()
    news = news.lower().split()
    news = [lemmatizer.lemmatize(word) for word in news if word not in stopwords]
    pred = mymodel.docvecs.most_similar(positive=[mymodel.infer_vector(news)], topn=2)    
    index = pred[0][0]
    if index==3460:
        index=pred[1][0]
    url = news_data[index]['link']['url']
    return url if pred[0][1] > THRESHOLD else None