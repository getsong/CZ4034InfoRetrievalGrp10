# CZ4034InfoRetrievalGrp10
The aim of this project is to perform the various tasks in the different stages of information retrieval and adopt different methods to enhance and optimise each stage. The stages include Crawling, Indexing and Querying and Classification. In this report, our group has selected Amazon Books as the target website for crawling, and use the crawled information for further processing.

## Python dependencies
Ensure Python and pip are installed on the machine and both are included in the path variable.

## Crawling
### Crawl links for books under the selected topic
To start crawling links, run:
```
cd CZ4034InfoRetrievalGrp10
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


## Querying
To install django, run:
```
pip install django
```

To start the django web server, run:
```
cd gui
python manage.py 

## Classification
To grab python packages for classification, run:
```
pip install scikitlearn
pip install pandas
pip install numpy
```

Ensure data is present in same directory: amazon_Stemmed.json
