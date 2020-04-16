import sys
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from sys_rarbg import sys_rarbg
from sys_rarbg.schedule import sys_rarbg_schedule

app = Flask(__name__)
app.register_blueprint(sys_rarbg.blueprint)
scheduler = BackgroundScheduler()
scheduler.start()

# Add scheduled jobs
sys_rarbg_schedule(scheduler.add_job)

if __name__ == '__main__':
  app.run(debug=True)