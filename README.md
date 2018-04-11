# CZ4034InfoRetrievalGrp10
The aim of this project is to perform the various tasks in the different stages of information retrieval and adopt different methods to enhance and optimise each stage. The stages include Crawling, Indexing and Querying and Classification. In this report, our group has selected Amazon Books as the target website for crawling, and use the crawled information for further processing.

## Python dependencies
Ensure Python and pip are installed on the machine and both are included in the path variable.

## Crawling
### Crawl links for books under the selected topic
To start crawling links, cd to the root folder and run:
```
cd crawl
python crawlLinks.py
```
crawlLinks.py now crawls links under cook-outdoor cooking. If links for other topics are to be crawled, change the parameters at line 18  and line 47 in the script.

### Crawl book details using the links
To start crawling book details, run:
```
python crawlBooks.py
```
Change the input (links) and output (book details) files if you want to crawl different topics.

## Indexing
To start indexing, cd to the root folder and run:
```
cd solr/solr-7.2.1/bin
solr start
```

Open a web browser and go to localhost:8983/solr, check whether there is a core called "amazon". If the core does not exist, run:
```
solr create -c amazon
cd ..
python solr_indexing.py
```

## Querying
To install django, run:
```
pip install django
```

To start the django web server, run:
```
cd gui
python manage.py runserver
```

Open a web browser and go to the link
```
127.0.0.1:8000
```

Type your query for the books, select the book categories and then enter/click the submit button for querying.

## Classification
To grab python packages for classification, run:
```
pip install scikitlearn
pip install pandas
pip install numpy
```

To run classification, cd to the root folder and run:
```
cd classification
python classification2.py
```
