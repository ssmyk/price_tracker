from flask import request
from flask.views import MethodView
from scraper_app.tasks.scraper import scraper_task

class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        scraper_task.delay('B07WKNQ8JT')
        return body