from flask import Flask
from sys_rargb import sys_rargb

app = Flask(__name__)
app.register_blueprint(sys_rargb.blueprint)

if __name__ == '__main__':
    app.run(debug=True)