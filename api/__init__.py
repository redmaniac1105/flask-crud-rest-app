from flask_restful import Api

from app import flaskAppInstance
from .task import Task, Task1

restServer = Api(flaskAppInstance)

restServer.add_resource(Task,"/api/v1.0/task")
restServer.add_resource(Task1,"/api/v1.0/task1/<author>")