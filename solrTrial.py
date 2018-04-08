# If on Python 2.X
from __future__ import print_function
import pysolr
import json

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/jcg/', timeout=10)

f = open("crawl/cook.json", 'r')
file = json.load(f)
solr.add(file)
# with open("crawl/cook.json", mode='r', encoding='utf-8') as feedsjson:
#     feeds = json.load(feedsjson)
#     solr.add(feeds)

# Later, searching is easy. In the simple case, just a plain Lucene-style
# query is fine.
results = solr.search('recipe')

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The title is '{0}'.".format(result['product_name']))
