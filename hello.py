from flask import Flask, redirect, url_for, request,render_template
from pymongo import MongoClient
import spacy
from flask_sqlalchemy import SQLAlchemy
from word2number import w2n
nlp = spacy.load("en_core_web_sm")
from autocorrect import Speller
from spacy.vocab import Vocab
vocab = Vocab()



connection=MongoClient()
db=connection['conf1']
collection=db['confall']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.static_folder = 'static'


class freq1(db.Model):
   id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   content = db.Column(db.String(200))
   freq = db.Column(db.Integer)
   def __init__(self, cn1):
      self.content = cn1
      self.freq=1


def get_nlp(query):
   spell = Speller(lang='en')
   query = query.lower()
   inc = ["paper", "conference", "show", "computer", "computing","conferences","research"]
   short_forms = {'ml': "machine learning artificial", 
                  "nlp":"natural language processing",
                  "cn":"networks", "dbms":"database",
                  "ai":"artificial intelligence","cs":"computer science",
                  "os":"operating system","cv":"computer vision",
                  "p2p":"peer to peer","it":"information technolgy",
                  "se":"software engineering","toc":"theory of computation",
                  "biotech":"bioinformatics biology","tech":"engineer",
                  "bioinformatics":"bioinformatics biology",
                  "bio":"biology"}


   doc = nlp(query)
   to_search=[]
   for i in doc:
      new_i = spell(i.text)
      print(new_i, i.pos_)
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
   recentQ = []
   res = freq1.query.order_by(freq1.freq).limit(5).all()
   res = freq1.query.order_by(freq1.freq)
   cnt=1
   for res2 in res[::-1]:
      res3=res2.content
      recentQ.append(res3)
      cnt+=1
      if cnt>=6:
         break
   return render_template('index.html',recentQ = recentQ)


dct = { "A*": "A1",
      "A": "A2",
       "B": "A3",
       'B':"A4",
       "C":"A5"  }
def srt(e):
   try:
      return dct[str(e["Rank"])]
   except KeyError:
      return e["Rank"]
@app.route("/index2", methods=['GET', 'POST'])
def index2():
   if request.method=="GET":
      query = request.args.get('query', None) 
      queries = get_nlp(query)
      st=""
      check_q= freq1.query.filter_by(content = query).first()
      if check_q:
         fr=check_q.freq
         check_q.freq =fr+1
         db.session.commit()
      else:
         new_q = freq1(query)
         db.session.add(new_q)
         db.session.commit()
      recentQ = []
      res = freq1.query.order_by(freq1.freq)
      cnt=1
      for res2 in res[::-1]:
         res3=res2.content
         recentQ.append(res3)
         cnt+=1
         if cnt>=6:
            break
      output = []
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
               url_fr = i["url_for"]
            except KeyError:
               url_fr = ""
            if query.lower() in title.lower():
               d = {}
               d["Title"] = title
               d["Acronym"] = Acronym
               d["Source"] = Source
               d["Rank"] = Rank
               d["Start_Date"] = startDate
               d["End_Date"] = endDate
               d["Location"] = location
               d["url_for"] = url_fr
               output.append(d)         
         output=sorted(output,key=srt)
         print(output)
      return render_template('index2.html', output=output, recentQ = recentQ)
   elif request.method=='POST':
      query = request.form['sField']
      print(query)
      return redirect(url_for("index2", query=query))


if __name__ == '__main__':
   db.create_all()
   app.run(port=8000,debug=True)
