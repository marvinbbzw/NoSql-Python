import os
from pymongo import MongoClient

uri = os.getenv("MONGO_URI")

if not uri:
    print("Umgebungsvariable nicht gesetzt.")
else:
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        info = client.server_info()
        print("Erfolgreich verbunden")
    except Exception as e:
        print("Verbindung fehlgeschlagen:", e)