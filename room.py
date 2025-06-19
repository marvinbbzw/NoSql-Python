class Room:
    def __init__(self, name, seats, is_reservable, _id = None):
        if(_id is not None):
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable


from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

info = client.server_info()
print("MongoDB-Version:", info["version"])

dblist = client.list_database_names()

for db in dblist:
	print(db)

dblist = client.list_database_names()

if "admin" in dblist:
    print("Database exists.")
else:
    print("Database does not exist.")
