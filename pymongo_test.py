import pymongo
import pandas as pd
from pandas.io.json import json_normalize
import re

mongodb_client = pymongo.MongoClient('mongodb://Marukun:marukun@localhost:27017')
mongodb_db = mongodb_client["crawler_db"]
mongodb_coll = mongodb_db["crawler_coll"]

return_docs = mongodb_coll.find_one()
print(return_docs)

ret = mongodb_coll.find()
for r in ret:
    print("id", r['id'])
    print("document_title", r['document_title'])
    print('document_attributes', r['document_attributes'])
    print('document_number', r['document_attributes']['Nomor'])
    print('document_ratification_date', r['document_attributes']['Tanggal Disahkan'])
    print('document_promulgation_date', r['document_attributes']['Tanggal Diundangkan'])
    print('lembaran_negara', r['document_attributes']['LN'])
    print('tambahan_lembaran_negara', r['document_attributes']['TLN'])
    print('pdf_filepath', r['document_attributes']['File'])
    print(type(r))
    print(type(r['document_attributes']))
    break

# df = json_normalize(ret)
# print(df)
# print(df.columns)

print("Document count:", mongodb_coll.count_documents(filter = {}))

print("Min document ID:", mongodb_coll.find_one(sort=[("id", 1)])["id"])
print("Max document ID:", mongodb_coll.find_one(sort=[("id", -1)])["id"])

# ret = mongodb_coll.find({"document_attributes":{"Referensi RUU": {'$regex':'*Data tidak ditemukan.*'}}})
# for r in ret:
#     print(r)

# ret = mongodb_coll.find({"document_title":""})
# for r in ret:
#     print(r)