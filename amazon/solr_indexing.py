# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 15:28:00 2018

@author: daq11
"""

import pysolr,json,argparse
parser = argparse.ArgumentParser(description='load json into python.')
parser.add_argument('C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/amazon/json_trial.json', metavar='input', type=str, help='json input file')
parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')

args = parser.parse_args()
solr = pysolr.Solr(args.solr_url, timeout=10)

items = json.load(open(args.input_file))
for item in items:
  item['id'] = item['url']

solr.add(items)