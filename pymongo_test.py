import pymongo

mongodb_client = pymongo.MongoClient('mongodb://Marukun:marukun@localhost:27017')
mongodb_db = mongodb_client["crawler_db"]
mongodb_coll = mongodb_db["crawler_coll"]

return_docs = mongodb_coll.find_one()

print(return_docs)

print("Document count:", mongodb_coll.count_documents(filter = {}))

print("Min document ID:", mongodb_coll.find_one(sort=[("id", 1)])["id"])
print("Max document ID:", mongodb_coll.find_one(sort=[("id", -1)])["id"])