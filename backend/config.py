import os
DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'auth.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY= 'This is secret'