import os
import sys
import requests
from flask import Blueprint, request, jsonify

# Conditionally import the correct configuration for the running environment
if os.getenv('FLASK_ENV') == 'development':
  from sys_qbittorrent.dev_config import config
else:
  from sys_qbittorrent.config import config

# Define a blueprint object, using the flask blueprint function
blueprint = Blueprint('sys_qbittorrent', __name__)


# ======================================================== #
# ====================== Member Data ===================== #
# ======================================================== #

# Define API path information
version = config['version']
baseUrl = '/sys/qbittorrent'

# JSON about payload
about = {
  'framework': 'flask',
  'runtime': '1.1',
  'author': 'Jordan Chappell',
  'contact': 'jordan.chappell33@gmail.com',
  'api': 'sys-qbittorrent',
  'version': version,
  'description': 'A Restful WebAPI to interact with qBittorrent WebUI',
  'environment': os.getenv('FLASK_ENV'),
}

# qBittorrent Request session info
qbittorrentCookieName = config['qbittorrentCookieName']
qbittorrentHost = config['qbittorrentHost']
qbittorrentBaseUrl = config['qbittorrentBaseUrl']
qbittorrentUsername = config['qbittorrentUsername']
qbittorrentPassword = config['qbittorrentPassword']

session = requests.Session()
session.headers = {'Referer': qbittorrentHost}

# ======================================================== #
# ======================= Functions ====================== #
# ======================================================== #

def check_auth_make_request(request):
  response = request() # attempt to make the request initially

  # check if the request was forbidden / unauthorized and then login
  if response.status_code == 403:
    session.post('{0}{1}/auth/login'.format(qbittorrentHost, qbittorrentBaseUrl),
     data={'username': qbittorrentUsername, 'password': qbittorrentPassword})
    response = request()

  return response.text, response.status_code

# ======================================================== #
# ====================== API Routes ====================== #
# ======================================================== #

# * /{version}/sys/qbittorrent/about
# * URI Parameters: N/A
# * Query Parameters: N/A
@blueprint.route('{0}{1}/about'.format(version, baseUrl), methods=['GET'])
def get_about():
  '''
  Returns information about the API and environment.
  '''
  return jsonify(about)

# * /{version}/sys/qbittorrent/torrents
# * URI Parameters: N/A
# * Query Parameters: N/A
@blueprint.route('{0}{1}/torrents'.format(version, baseUrl), methods=['GET','POST'])
def torrents():
  if request.method == 'GET':
    '''
    Return a list of all torrents currently being downloaded/seeded in qBittorrent
    '''
    response = check_auth_make_request(
      lambda: session.get('{0}{1}/torrents/info'.format(qbittorrentHost, qbittorrentBaseUrl)))
    return response

  else:
    '''
    Add a torrent(s) to download by URL(s)
    '''
    requestData = request.get_json()  # get the JSON body of the request
    try:
      torrentLinks = requestData['urls'] # if request body does not contain a 'urls' object then the except clause will run
      data = {
        'urls': torrentLinks
      }
      response = check_auth_make_request(
        lambda: session.post('{0}{1}/torrents/add'.format(qbittorrentHost, qbittorrentBaseUrl), data))
      return response
    except:
      message = {
        'message': 'missing required data for \'urls\' in body of request, data should be valid torrent link(s)/url(s)'
      }
      status_code = 400  
      return message, status_code
    



