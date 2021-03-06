# Conference-Ranker


## Project Information:
To design and develop a conference ranking system that fetches a list of conferences according to the search keywords given as input.


## Workflow:

* Fetching of data using APIs and populating the database 
   * Integration of Python and MongoDB using PyMongo
   * CSV data from CORE conference is populated into MongoDB and then exported from MongoDB into json format


* Design of front-end and display of conference data:
   * An easy-to-use front-end is designed using HTML, CSS, JavaScript and Bootstrap. 
   * Based on the search keywords, the list of conferences are fetched from the database. 
   * The list of conferences and their information is displayed.
        

* Implementation of semantic search:
   * NLP-based techniques are used to implement semantic search.
   * Semantic search utilizes the meaning of the search keywords along with contextual information, unlike lexical search where only literal matching of the keyword is done.


### How to run the project

Run the following commands in order from the **Conference-Ranker-Main** directory

`pip install virtualenv`

`virtualenv env`

`source ./env/bin/activate`


`pip install -r requirements.txt`

`python3 hello.py`

`python -m spacy download en_core_web_sm`

Install mongodb and import confall.json in `conf1` database as `confall` collection

-----------------------

**Made By Penta Squad**
