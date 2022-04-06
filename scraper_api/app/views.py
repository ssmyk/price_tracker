from celery.utils.log import get_task_logger
from flask import request
from flask.views import MethodView
import requests

from .scraper import scraper_task, celery_app, scraper_task_update

get_task_logger = get_task_logger(__name__)


class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'], body['user_id'])
        print(task.id)

        return {"task_id": task.id}

    def get(self):
        resp = requests.get('http://web_app:5000/products/')
        products = resp.json()
        for product in products:
            asin = product['product_asin']
            user_id = product['fk_user']
            scraper_task_update.delay(asin, user_id)
        return f'Number of updating products:{len(products)}'


class TaskStatus(MethodView):
    def get(self, task_id):
        task = celery_app.AsyncResult(task_id)
        print(task.status)
        result = {'task_status': task.status}

        return result
