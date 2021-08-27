from flask import jsonify, request
from flask_restful import Resource
from app import mongo
import logging as logger

class Task1(Resource):
    def get(self,author):
        content = mongo.db.content

        output = []

        q = content.find_one({'author' : author})
        if q:
            output = {'author' : q['author'], 'title' : q['title'], 'blog' : q['blog']}
        else:
            output = 'Not found'
        return jsonify({'result' : output}) 


class Task(Resource):       
    def get(self):
        content = mongo.db.content

        output = []

        for q in content.find():
            output.append({'author' : q['author'], 'title' : q['title'], 'blog' : q['blog']})

        return jsonify({'result' : output})

    def post(self):
        content = mongo.db.content

        author = request.json['author']
        title = request.json['title']
        blog = request.json['blog']

        content.insert({'author' : author, 'title' : title, 'blog' : blog})
        return 'Successful Insertion'
    def patch(self):
        author = request.json['author']

        content = mongo.db.content

        content.update({'author' : author },
                    {'author': 'Harry',
                    'title': 'Second Blog',
                    'blog': 'Hello everyone welcome to my first blog. Update: actually second'
                            })
        return 'Insertion Successful'

    def delete(self):
        author = request.json['author']

        content = mongo.db.content

        content.remove({'author' : author })

        return 'Deletion Successful'