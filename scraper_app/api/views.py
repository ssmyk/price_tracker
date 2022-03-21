from flask import request
from flask.views import MethodView

class AddTaskAPI(MethodView):
    def post(self):
        body = request.json
