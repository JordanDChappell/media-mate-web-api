import os
import sys
import feedparser
from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from utils.request_validation import required_query_params

# Conditionally import the correct configuration for the running environment
if os.getenv('FLASK_ENV') == 'development':
  from dev_config import config
else:
  from config import config

# Define a blueprint object, using the flask blueprint function
blueprint = Blueprint('sys_rargb', __name__)

# Set up MongoDB client
dbClient = MongoClient()
db = dbClient.flaskdb

# Define API path information
version = config['version']
baseUrl = '/sys/rargb'

# JSON about payload
about = {
  'framework': 'flask',
  'runtime': '1.1',
  'author': 'Jordan Chappell',
  'contact': 'jordan.chappell33@gmail.com',
  'api': 'sys-rargb',
  'version': version,
  'description': 'A Restful WebAPI to serve RARGB feeds',
  'environment': os.getenv('FLASK_ENV'),
}

########################
###### API ROUTES ######
########################

# /{version}/sys/rargb/about
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/about'.format(version, baseUrl), methods=['GET'])
def get_about():
  '''
  Returns information about the API and environment
  '''
  return jsonify(about)

# /{version}/sys/rargb/feeds/categories
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/feeds/categories'.format(version, baseUrl), methods=['GET', 'PUT'])
def feeds():
  feedsCollection = db.feeds
  if request.method == 'PUT':
    '''
    Update the categories that sys-rargb is using to update the torrent list
    '''
    data = request.get_json()
    try:
      newCategories = data['categories']
      feedsCollection.update({'name': 'categories'},{'$set': {'value': newCategories}})
      message = {
        'message': 'success',
        'categories': newCategories
      }
      status_code = 200
    except:
      message = {
        'message': 'missing required data for \'categories\''
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

########################
####### API JOBS #######
########################  
