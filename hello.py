from flask import Flask, redirect, url_for, request
# from flask.templating import render_template
from flask import Flask, render_template, request
from pymongo import MongoClient
import spacy
import numpy
from word2number import w2n
nlp = spacy.load("en_core_web_sm")
from autocorrect import Speller
from spacy.vocab import Vocab
vocab = Vocab()

connection=MongoClient()
#db=connection['conf1']
#collection=db['confall']
db=connection['conf']
collection=db['conf2']


app = Flask(__name__)
app.static_folder = 'static'

# query="test_data"
def get_nlp(query):
   spell = Speller(lang='en')
   query = query.lower()
   inc = ["paper", "conference", "show", "computer", "computing"]
   short_forms = {'ml': "machine learning", "nlp":"natural language processing",
                  "cn":"networks", "dbms":"database",
                  "ai":"artificial intelligence"}


   doc = nlp(query)
   to_search=[]
   for i in doc:
      new_i = spell(i.text)
      print(new_i, i.pos_)
      # print(i, i.pos_, i.lemma_)
      if(new_i in short_forms.keys()):
         z = short_forms[new_i].split()
         for new_i in z:
               to_search.append(new_i)
         continue

      if((i.pos_ == "NOUN" or i.pos_=="VERB") and (i.lemma_ not in inc)):
         to_search.append(i.text)
      
   return to_search


@app.route('/', methods=['GET', 'POST'])
def hello_world():
   if request.method=='POST':
      query = request.form['sField']
      print(query)
      return redirect(url_for("index2", query=query))
   return render_template('index.html')

from flask import Flask, url_for
@app.route("/index2", methods=['GET', 'POST'])
def index2():
   if request.method=="GET":
      query = request.args.get('query', None) 
      recentQ = []
      print(query)
      recentQ.append(query)
      output = []
      queries = get_nlp(query)
      for query in queries:
         for i in collection.find():
            title = i["Title"]
            try:
               Acronym = i["Acronym"]
            except KeyError:
               Acronym = ""
            try:
               Source = i["Source"]
            except KeyError:
               Source = ""
            try:
               Rank = i["Rank"]
            except KeyError:
               Rank = ""
            # try:
            #    hasData = i["hasData"]
            # except KeyError:
            #    hasData = ""
            # try:
            #    PrimaryFor = i["Primaryfor"]
            # except KeyError:
               # PrimaryFor = ""
            try:
               startDate = i["Start_Date"]
            except:
               startDate = ""
            try:
               endDate = i["End_Date"]
            except:
               endDate=""
            try:
               location = i["Location"]
            except:
               location="" 
            try:
               url_for1 = i["url_for"]
            except KeyError:
               url_for1 = ""
            if query.lower() in title.lower():
               d = {}
               d["Title"] = title
               d["Acronym"] = Acronym
               d["Source"] = Source
               d["Rank"] = Rank
               d["Start_Date"] = startDate
               d["End_Date"] = endDate
               d["Location"] = location
               d["url_for"] = url_for1
               output.append(d)
         print(output)
      return render_template('index2.html', output=output, recentQ = recentQ)
   if request.method=="POST":
      query1 = request.form['sField']
      print(query1)
      return redirect(url_for("index2", query=query1))
      



if __name__ == '__main__':
   app.run(port=8000,debug=True)
