from flask import Flask, redirect, url_for, request
# from flask.templating import render_template
from flask import Flask, render_template, request
from pymongo import MongoClient


connection=MongoClient()
db=connection['conf']
collection=db['conf2021']

app = Flask(__name__)
app.static_folder = 'static'

# query="test_data"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   if request.method=='POST':
      query = request.form['sField']
      print(query)
      return redirect(url_for("index2", query=query))
   return render_template('index.html')

@app.route("/index2", methods=['GET', 'POST'])
def index2():
   if request.method=="GET":
      query = request.args.get('query', None) 
      print(query)
      output = []
      for i in collection.find():
         title = i["Title"]
         Acronym = i["Acronym"]
         Source = i["Source"]
         Rank = i["Rank"]
         hasData = i["hasData"]
         PrimaryFor = i["Primaryfor"]
         url_for = i["url_for"]
         if query.lower() in title.lower():
            d = {}
            d["Title"] = title
            d["Acronym"] = Acronym
            d["Source"] = Source
            d["Rank"] = Rank
            d["hasData"] = hasData
            d["Primaryfor"] = PrimaryFor
            d["url_for"] = url_for
            output.append(d)

      print(output)
      return render_template('index2.html', output=output)

if __name__ == '__main__':
   app.run()
