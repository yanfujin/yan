import os

DEBUG= True
SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@127.0.0.1:3306/yan'
SQLALCHEMY_TRACK_MODIFICATIONS = False



