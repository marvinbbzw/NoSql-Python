from pymongo import MongoClient
from bson import ObjectId
import os

client = MongoClient("mongodb+srv://marvin:20.Berta.08@cluster1.ggkeq.mongodb.net/?retryWrites=true&w=majority")

def clear(): os.system("cls" if os.name == "nt" else "clear")
def pause(): input("Press any button to return"); main()

def select_from_list(title, items, prompt):
    if not items:
        print(f"No {title}")
        pause()
    print(f"{title}")
    for item in items:
        print(f" - {item}")
    selected = input(f"\n{prompt}: ").strip()
    if selected not in items:
        print(f"{title[:-1]} not found.")
        return select_from_list(title, items, prompt)
    return selected

def parse_id(val):
    try:
        return ObjectId(val)
    except:
        try:
            return int(val)
        except:
            return val

def main():
    clear()

    db_name = select_from_list("Databases", client.list_database_names(), "Select Database")
    db = client[db_name]

    clear()

    col_name = select_from_list("Collections", db.list_collection_names(), "Select Collection")
    col = db[col_name]

    clear()

    docs = list(col.find({}, {"_id": 1}))
    doc_ids = [str(doc["_id"]) for doc in docs]
    doc_id_input = select_from_list("Documents", doc_ids, "Select Document")
    doc_id = parse_id(doc_id_input)

    clear()

    doc = col.find_one({"_id": doc_id})
    if not doc:
        print("Document not found.")
        pause()
    print(f"{db_name}.{col_name}.{doc_id}\n")
    for k, v in doc.items():
        print(f"{k}: {v}")
    pause()

if __name__ == "__main__":
    main()