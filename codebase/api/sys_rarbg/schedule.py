import sys
import feedparser
import datetime
from pymongo import MongoClient

# Set up MongoDB client
dbClient = MongoClient()
db = dbClient.flaskdb

########################
####### API JOBS #######
########################  

def read_rarbg_rss():
  '''
  A scheduled job to read the RARBG rss feed and store information about new torrents that fit criteria listed in database
  '''
  # Retrieve the currently stored torrents from database
  torrentCollection = db.rsstorrents
  torrents = torrentCollection.find()

  # Retrieve the feeds options collection and determine the categories to retrieve from RARBG
  feedsCollection = db.feeds
  categories = db.feeds.find_one({'name': 'categories'})['value'] # list of category values
  filters = db.feeds.find_one({'name': 'filters'})['value'] # list of filter values

  # Get the RARBG rss feed for torrents in the given category and insert anything that matches filters and current + previous year
  rarbgRss = feedparser.parse('http://rarbg.to/rssdd.php?categories={0}'.format(';'.join(categories)))
  torrentsToAdd = match_torrents(rarbgRss['entries'], filters)

  for torrent in torrentsToAdd:
    query = torrentCollection.update_one({'title': torrent['title']}, {'$setOnInsert': {'link': torrent['link']}}, upsert=True)
    print(query, file=sys.stdout)

# Set up background scheduler to run API background jobs
def sys_rarbg_schedule(add_job):
  '''
  add_job is a function of APScheduler, sent from app.py
  '''
  add_job(func=read_rarbg_rss, trigger="interval", minutes=1)

#######################
######## UTILS ########
####################### 

def match_torrents(torrents, filters):
  '''
  Utility function to match a torrent title to a list of filters and return a list of matched items
  '''
  torrentsToAdd = []

  # Determine current and previous year to use as a filter on movie release date
  currentYear = datetime.datetime.now().year

  # Check the torrent for a match on release year and filter
  for torrent in torrents:
      if (str(currentYear) in torrent['title'] or str(currentYear - 1) in torrent['title']):
        filtersMatched = 0
        for filter in filters:
          if filter in torrent['title']:
            filtersMatched += 1
        if filtersMatched == len(filters):
          torrentsToAdd.append({'title': torrent.title, 'link': torrent.link})

  return torrentsToAdd