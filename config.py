import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:HelloWorld123@tflappdatabase.cceacacihiv0.us-east-1.rds.amazonaws.com/tflappdatabaseRDS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False