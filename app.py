from flask import Flask
from flask_pymongo import PyMongo
import logging as logger
logger.basicConfig(level="DEBUG")

flaskAppInstance = Flask(__name__)
#flaskAppInstance.config["MONGO_URI"] = "mongodb+srv://redmaniac:redmaniac@vrblog.d5fnr.mongodb.net/VRBlog?retryWrites=true&w=majority"

#mongo = PyMongo(flaskAppInstance) 

if __name__ == '__main__':
    logger.debug("Starting the app")
    from api import *
    flaskAppInstance.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
