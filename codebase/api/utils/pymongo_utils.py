# file:         pymongo_utils.py
# description:  Utility functions for common pymongo methods

def cursor_to_list(cursor):
  '''
  Create a python list from a MongoDB cursor object, converting ObjectId to string where required
  '''
  list = []
  for document in cursor:
    document['_id'] = str(document['_id'])
    list.append(document)
  return list