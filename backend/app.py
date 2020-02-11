from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

#Authorization section
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
from transaction import *

if __name__ == '__main__':
	app.run()