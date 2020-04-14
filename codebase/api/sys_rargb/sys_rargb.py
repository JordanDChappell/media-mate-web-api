import os
import sys
from flask import Blueprint, request, jsonify
from utils.request_validation import required_query_params

# Conditionally import the correct configuration for the running environment
if os.getenv('FLASK_ENV') == 'development':
    from dev_config import config
else:
    from config import config

# Define a blueprint object, using the flask blueprint function
blueprint = Blueprint('sys_rargb', __name__)

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

# /{version}/sys/rargb/about
# URI Parameters: N/A
# Query Parameters: N/A
@blueprint.route('{0}{1}/about'.format(version, baseUrl), methods=['GET'])
def get_about():
    """ Returns information about the API and environment """
    return jsonify(about)

# /{version}/sys/rargb/feeds
# URI Parameters: N/A
# Query Parameters: 
# - categories: type: list
#               objects: number
@blueprint.route('{0}{1}/feeds'.format(version, baseUrl), methods=['GET'])
def get_feeds():
    """ Retrieve RSS objects from RARGB """
    message = required_query_params(request, ['categories'])
    if message is None:
      categories = request.args.get('categories')
      return jsonify({
        'categories': categories
      })
    else:
      return message