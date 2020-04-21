import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

from sys_rarbg import sys_rarbg
from sys_rarbg.schedule import sys_rarbg_schedule
from sys_qbittorrent import sys_qbittorrent

# Define the app as a flask application
app = Flask('mediamate')

# Set up logger handling in Flask
logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
app.logger.addHandler(consoleHandler)

fileHandler = RotatingFileHandler('mediamate.log', maxBytes=2000, backupCount=10)
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.ERROR)
app.logger.addHandler(fileHandler)

# Set up Cross Origin Resource Sharing
CORS(app)

# Register blueprints
app.register_blueprint(sys_rarbg.blueprint)
app.register_blueprint(sys_qbittorrent.blueprint)

# Add scheduled jobs
scheduler = BackgroundScheduler()
scheduler.start()
sys_rarbg_schedule(scheduler.add_job)

if __name__ == '__main__':
  app.run()