import os
import sys
from flask import Blueprint, request, jsonify
from utils.request_validation import required_query_params

# Define a blueprint object, using the flask blueprint function
blueprint = Blueprint('sys_rargb', __name__)

# Define API path information
version = os.getenv('API_VERSION')
baseUrl = '/sys/rargb'

# JSON about payload
about = {
  'framework': 'flask',
  'runtime': '1.1',
  'author': 'Jordan Chappell',
  'contact': 'jordan.chappell33@gmail.com',
  'description': 'A Restful WebAPI to serve RARGB feeds',
  'environment': os.getenv('FLASK_ENV')
}

@blueprint.route('{0}{1}/about'.format(version, baseUrl), methods=['GET'])
def get_about():
    return jsonify(about)

@blueprint.route('{0}{1}/feeds'.format(version, baseUrl), methods=['GET'])
def get_feeds():
    """ Retrieve RSS objects from RARGB """
    message = required_query_params(request, ['categories'])
    if message is None:
        
    else:
        return message