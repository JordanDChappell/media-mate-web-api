import os
import feedparser
import requests
from utils import db_client
from utils.logger import get_logger

# Conditionally import the correct configuration for the running environment
if os.getenv('FLASK_ENV') == 'development':
  from sys_rarbg.dev_config import config
else:
  from sys_rarbg.config import config

# ======================================================== #
# ====================== Member Data ===================== #
# ======================================================== #

# Set up logger
logger = get_logger(__name__)

# Set up MongoDB client
db = db_client.flaskdb

# TMDb API information
tmdbHost = config['tmdbHost']
tmdbBaseUrl = config['tmdbBaseUrl']
tmdbApiKey = config['tmdbApiKey']

#TMDb poster information
tmdbPosterBasePath = config['tmdbPosterBasePath'],
tmdbPosterSize = config['tmdbPosterSize']

# ======================================================== #
# ======================= API Jobs ======================= #
# ======================================================== #

def read_rarbg_rss():
  '''
  A scheduled job to read the RARBG rss feed and store information about new torrents that fit criteria listed in database
  '''
  logger.info('Start of read_rarbg_rss job')

  # Retrieve the currently stored torrents from database
  torrentCollection = db.rsstorrents
  torrents = torrentCollection.find()

  # Retrieve the feeds options collection and determine the categories to retrieve from RARBG
  feedsCollection = db.feeds
  categories = db.feeds.find_one({'name': 'categories'})['value'] # list of category values
  filters = db.feeds.find_one({'name': 'filters'})['value'] # list of filter values

  # Get the RARBG rss feed for torrents in the given category and filter for anything that matches current filters
  rarbgRss = feedparser.parse('http://rarbg.to/rssdd.php?categories={0}'.format(';'.join(categories))) # Read the RARBG RSS feed with given categories
  torrents = rarbgRss['entries']
  torrentsToAdd = filter_torrents(torrents, filters)  # Match torrents to the set filters
  torrentsToAdd = parse_torrent_information(torrentsToAdd)  # Parse the torrent title for movie info: name, release year, resolution

  logger.info('{0} torrents that match filter criteria'.format(len(torrentsToAdd)))

  for torrent in torrentsToAdd:
    query = torrentCollection.update_one({'title': torrent['title']}, 
    {'$setOnInsert': { 
      'link': torrent['link'],
      'displayName': torrent['displayName'],
      'releaseYear': torrent['releaseYear'],
      'resolution': torrent['resolution'],
      'posterLink': torrent['posterLink'] }
    }, upsert=True)
    logger.info(query)

  logger.info('End of read_rarbg_rss job')

# Set up background scheduler to run API background jobs
def sys_rarbg_schedule(add_job):
  '''
  add_job is a callback function of APScheduler, sent from app.py, add any functions that should be scheduled here
  '''
  add_job(func=read_rarbg_rss, trigger="interval", minutes=10)

# ======================================================== #
# ======================= Functions ====================== #
# ======================================================== #

def filter_torrents(torrents, filters):
  '''
  Utility function to filter a list of torrents by the values in the filter list
  '''
  filteredTorrents = torrents.copy()

  for filterValue in filters:
    filteredTorrents = list(filter(lambda torrent: filterValue in torrent['title'], filteredTorrents))

  return filteredTorrents

def parse_torrent_information(torrentsToModify):
  '''
  Utility function used to format a display/readable title from the torrent title obtained from RARBG
  E.g Toy.Story.4.2018.1080p.BluRay.H264.AAC-RARBG -> { 'displayName': 'Toy Story 4', 'releaseYear': '2018', 'resolution': '1080p' }
  Requests a movie poster for each torrent from TMDb where applicable
  '''
  modifiedTorrents = []

  # Loop over the list of torrents and parse the title, assuming the same format for all RARBG torrents
  for torrent in torrentsToModify:
    featuresArray = torrent['title'].split('.') # Extract the features from the torrent title by splitting on '.'
    resolution = featuresArray[-4]
    releaseYear = featuresArray[-5]
    displayName = ' '.join(featuresArray[0:-5])
    posterPath = request_tmdb_poster(displayName)
    posterLink = '{0}{1}{2}'.format(tmdbPosterBasePath, tmdbPosterSize, posterPath) if posterPath != '' else ''

    # Append the new torrent
    modifiedTorrents.append({
      'title': torrent['title'],
      'link': torrent['link'],
      'displayName': displayName,
      'releaseYear': releaseYear,
      'resolution': resolution,
      'posterLink': posterLink
    })

  return modifiedTorrents

def request_tmdb_poster(searchQuery):
  '''
  Makes a request to TMDb API for a movie poster by the given search query
  '''
  requestUrl = '{0}{1}/search/movie?api_key={2}&include_adult=false&query={3}'.format(tmdbHost, tmdbBaseUrl, tmdbApiKey, searchQuery)
  response = requests.get(requestUrl)
  
  if response.ok:
    json = response.json()
    if json['total_results'] > 0:
      return json['results'][0]['poster_path']
  else:
    logger.error('TMDb request failed, status code: {0}, message: {1}'.format(response.status_code, response.json()['status_message']))
    
  return ''