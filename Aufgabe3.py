from pymongo import MongoClient
from datetime import datetime
import re

client = MongoClient("mongodb+srv://marvin:20.Berta.08@cluster1.ggkeq.mongodb.net/?retryWrites=true&w=majority")
db = client["restaurant"]
collection = db["restaurants"]

def zeige_bezirke():
    print("Stadtbezirke:")
    for b in collection.distinct("borough"):
        print("-", b)

def top3_restaurants():
    print("\nTop 3 Restaurants:")
    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {"_id": "$name", "avg": {"$avg": "$grades.score"}}},
        {"$sort": {"avg": -1}},
        {"$limit": 3}
    ]
    for r in collection.aggregate(pipeline):
        print(f"{r['_id']}: {round(r['avg'], 2)}")

def naechstes_zu_perigord():
    print("\nSuche nächstes Restaurant zu Le Perigord")
    collection.create_index([("address.coord", "2dsphere")])
    perigord = collection.find_one({"name": "Le Perigord"})
    if not perigord:
        print("Nicht gefunden.")
        return
    punkt = {"type": "Point", "coordinates": perigord["address"]["coord"]}
    ergebnis = collection.find_one({
        "name": {"$ne": "Le Perigord"},
        "address.coord": {"$near": {"$geometry": punkt}}
    })
    if ergebnis:
        print("Nächstes Restaurant:", ergebnis["name"])

def suche_restaurants():
    print("\nRestaurant-Suche")
    name = input("Name enthält (optional): ")
    kueche = input("Küche enthält (optional): ")

    suche = {}
    if name:
        suche["name"] = {"$regex": re.escape(name), "$options": "i"}
    if kueche:
        suche["cuisine"] = {"$regex": re.escape(kueche), "$options": "i"}

    ergebnisse = list(collection.find(suche).limit(10))
    if not ergebnisse:
        print("Keine gefunden.")
        return None

    for i, r in enumerate(ergebnisse):
        print(f"[{i}] {r['name']} | {r['cuisine']} | {r['borough']}")

    try:
        wahl = int(input("Nummer für Bewertung (Enter = abbrechen): "))
        return ergebnisse[wahl]["_id"]
    except:
        return None

def bewerten(restaurant_id):
    if not restaurant_id:
        return
    try:
        score = int(input("Bewertung (0–10): "))
        if 0 <= score <= 10:
            collection.update_one(
                {"_id": restaurant_id},
                {"$push": {"grades": {"score": score, "date": datetime.utcnow()}}}
            )
            print("Bewertung gespeichert.")
        else:
            print("Ungültiger Wert.")
    except:
        print("Fehler bei der Eingabe.")

def main():
    zeige_bezirke()
    top3_restaurants()
    naechstes_zu_perigord()
    r_id = suche_restaurants()
    if r_id:
        bewerten(r_id)

main()
