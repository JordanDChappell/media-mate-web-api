from pymongo import MongoClient

client = MongoClient()

# ~~~~~~~~~~~~~~~ Databases ~~~~~~~~~~~~~~~ #
flaskdb = client.flaskdb # Flask AppDB, all flask application collections will be held here
