import collections
from collections import defaultdict
from itertools import combinations, chain
import json
from pprint import pprint

NER_data = []
with open('unique_NER_results.jsl') as name_entity_file:
    for items in name_entity_file:
        NER_data.append(json.loads(items))
        
co_occur =  [item['names']['ORGANIZATION'] for item in NER_data]        

def calculate_cooccurrence(data):
    counted_documents =  open('counted_documents.txt', 'a+') 
    result = collections.defaultdict(collections.Counter)
    for line in data:
        for char in line:
            result[char].update([c for c in line if c is not char])
    counted_documents.write(json.dumps(result) + '\n')
    counted_documents.flush()    

calculate_cooccurrence(co_occur)