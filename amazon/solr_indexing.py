# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 15:28:00 2018

@author: daq11
"""

import pysolr,json,argparse
# =============================================================================
# parser = argparse.ArgumentParser(description='load json into python.')
# parser.add_argument('C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/preprocess/amazon_Stemmed.json', metavar='input', type=str, help='json input file')
# parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')
# 
# args = parser.parse_args()
# solr = pysolr.Solr(args.solr_url, timeout=10)
# 
# items = json.load(open(args.input_file))
# for item in items:
#   item['id'] = item['url']
# 
# solr.add(items)
# =============================================================================



solr_instance = pysolr.Solr('http://localhost:8983/solr/amazon', timeout=10)
json_filename = 'C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/preprocess/amazon_Stemmed.json'
argws = {
    'commit': 'true',
    'extractOnly': False,
    'Content-Type': 'application/json',
}
with open(json_filename, 'rb') as f:
    solr_instance.extract(f, **argws)
    solr_instance.commit()

with open(json_filename, mode='r', encoding='utf-8') as feedsjson:    
    items = json.load(feedsjson)
for item in items:
  item['id'] = item['url']

solr_instance.add(items)