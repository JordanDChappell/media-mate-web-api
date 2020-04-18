import os
import sys
import feedparser
from pymongo import MongoClient
from flask import Blueprint, request, jsonify

from utils.request_validation import required_query_params
from utils.pymongo_utils import cursor_to_list

# Conditionally import the correct configuration for the running environment
if os.getenv('FLASK_ENV') == 'development':
  from sys_rarbg.dev_config import config
else:
  from sys_rarbg.config import config

# Define a blueprint object, using the flask blueprint function
blueprint = Blueprint('sys_rarbg', __name__)

# ======================================================== #
# ====================== Member Data ===================== #
# ======================================================== #

# Set up MongoDB client
dbClient = MongoClient()
db = dbClient.flaskdb

# Define API path information
version = config['version']
baseUrl = '/sys/rarbg'

# JSON about payload
about = {
  'framework': 'flask',
  'runtime': '1.1',
  'author': 'Jordan Chappell',
  'contact': 'jordan.chappell33@gmail.com',
  'api': 'sys-rarbg',
  'version': version,
  'description': 'A Restful WebAPI to serve rarbg feeds',
  'environment': os.getenv('FLASK_ENV'),
}

# ======================================================== #
# ====================== API Routes ====================== #
# ======================================================== #

# /{version}/sys/rarbg/about
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/about'.format(version, baseUrl), methods=['GET'])
def get_about():
  '''
  Returns information about the API and environment
  '''
  return jsonify(about)

# /{version}/sys/rarbg/feeds/categories
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/feeds/categories'.format(version, baseUrl), methods=['GET', 'PUT'])
def feeds_categories():
  feedsCollection = db.feeds  # mongodb collection 'feeds'
  if request.method == 'PUT':
    '''
    Update the categories that sys-rarbg is using to update the torrent list
    '''
    requestData = request.get_json()  # get the JSON body of the request
    try:
      newCategories = requestData['categories'] # if request body does not contain a 'categories' object then the except clause will run
      feedsCollection.update({'name': 'categories'}, {'$set': {'value': newCategories}}, upsert=True) # overwrite any objects in the feeds collection with name = categories
      message = {
        'message': 'success',
        'categories': newCategories
      }
      status_code = 200
    except:
      message = {
        'message': 'missing required data for \'categories\' in body of request'
      }
      status_code = 400     
    return message, status_code
    
  else:
    '''
    Return the list of categories currently being tracked
    '''
    categories = feedsCollection.find_one({'name': 'categories'})
    return jsonify({
      'categories': categories['value']
    })

# /{version}/sys/rarbg/feeds/filters
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/feeds/filters'.format(version, baseUrl), methods=['GET', 'PUT'])
def feeds_filters():
  feedsCollection = db.feeds  # mongodb collection 'feeds'
  if request.method == 'PUT':
    '''
    Update the filters that sys-rarbg is using to update the torrent list
    '''
    requestData = request.get_json()  # get the JSON body of the request
    try:
      newFilters = requestData['filters'] # if request body does not contain a 'filters' object then the except clause will run
      feedsCollection.update({'name': 'filters'}, {'$set': {'value': newFilters}}, upsert=True) # overwrite any objects in the feeds collection with name = filters
      message = {
        'message': 'success',
        'filters': newFilters
      }
      status_code = 200
    except:
      message = {
        'message': 'missing required data for \'filters\' in body of request'
      }
      status_code = 400  
    return message, status_code

  else:
    '''
    Return the list of filters currently being tracked
    '''
    filters = feedsCollection.find_one({'name': 'filters'})
    return jsonify({
      'filters': filters['value']
    })

# /{version}/sys/rarbg/torrents
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/torrents'.format(version, baseUrl), methods=['GET'])
def get_torrents():
  torrentCollection = db.rsstorrents
  torrents = cursor_to_list(torrentCollection.find())
  return jsonify({
    'torrents': torrents
  })
