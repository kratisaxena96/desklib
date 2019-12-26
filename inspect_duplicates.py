#!/usr/local/bin/python3

# A description and analysis of this code can be found at
# https://alexmarquardt.com/2018/07/23/deduplicating-documents-in-elasticsearch/

import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch(["localhost:9200/"])
dict_of_duplicate_docs = {}

keys_to_include_in_hash = ["title","description","summary"]


# Process documents returned by the current search/scroll
def populate_dict_of_duplicate_docs(hits):
    for item in hits:
        combined_key = ""
        for mykey in keys_to_include_in_hash:
            combined_key += str(item['_source'][mykey])

        _id = item["_id"]

        hashval = hashlib.md5(combined_key.encode('utf-8')).digest()

        dict_of_duplicate_docs.setdefault(hashval, []).append(_id)


def scroll_over_all_docs():
    data = es.search(index="haystack_new", scroll='1m',  body={"query": {"match_all": {}}})
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    populate_dict_of_duplicate_docs(data['hits']['hits'])

    while scroll_size > 0:
        data = es.scroll(scroll_id=sid, scroll='2m')

        populate_dict_of_duplicate_docs(data['hits']['hits'])

        # Update the scroll ID
        sid = data['_scroll_id']

        scroll_size = len(data['hits']['hits'])


def loop_over_hashes_and_remove_duplicates():
    for hashval, array_of_ids in dict_of_duplicate_docs.items():
      if len(array_of_ids) > 1:
        print("********** Duplicate docs hash=%s **********" % hashval)
        # Get the documents that have mapped to the current hasval
        matching_docs = es.mget(index="haystack_new", doc_type="doc", body={"ids": array_of_ids})
        for doc in matching_docs['docs']:
            import pdb; pdb.set_trace()
            es.delete(index="haystack_new", doc_type="modelresult", id=doc['_id'])
            print("doc=%s\n" % doc)

def main():
    scroll_over_all_docs()
    loop_over_hashes_and_remove_duplicates()
    print(dict_of_duplicate_docs)


main()