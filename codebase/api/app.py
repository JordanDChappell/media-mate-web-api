import sys
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from sys_rarbg import sys_rarbg
from sys_rarbg.schedule import sys_rarbg_schedule
from sys_qbittorrent import sys_qbittorrent

# Define the app as a flask application and register required blueprints
app = Flask(__name__)
app.register_blueprint(sys_rarbg.blueprint)
app.register_blueprint(sys_qbittorrent.blueprint)

# Add scheduled jobs
scheduler = BackgroundScheduler()
scheduler.start()
# sys_rarbg_schedule(scheduler.add_job)

if __name__ == '__main__':
  app.run(debug=True)