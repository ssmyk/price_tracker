from celery.utils.log import get_task_logger
from flask import request
from flask.views import MethodView

from .scraper import scraper_task, celery_app

get_task_logger = get_task_logger(__name__)


class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'], body['user_id'])
        print(task.id)

        return {"task_id": task.id}


class TaskStatus(MethodView):
    def get(self, task_id):
        task = celery_app.AsyncResult(task_id)
        print(task.status)
        result = {'task_status': task.status}

        return result
