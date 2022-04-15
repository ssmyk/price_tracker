from celery.utils.log import get_task_logger
from flask import request
from flask.views import MethodView
import requests
from decouple import config

from .scraper import scraper_task_add, celery_app, scraper_task_update

get_task_logger = get_task_logger(__name__)


class ScraperAPI(MethodView):
    """
    API which allows to start celery tasks.
    """

    def post(self) -> dict:
        """
        Starts a celery task to scrap new product details and add it to tracking.
        """
        body = request.json
        task = scraper_task_add.delay(body["asin"], body["user_id"])
        return {"task_id": task.id}

    def patch(self) -> str:
        """
        Updates information of all tracked products in database.
        """
        resp = requests.get(config("API_PRODUCTS_GET"))
        products = resp.json()
        for product in products:
            asin = product["product_asin"]
            user_id = product["fk_user"]
            scraper_task_update.delay(asin, user_id)
        return f"Number of updating products:{len(products)}"


class TaskStatus(MethodView):
    """
    Used to retrieve current celery task status.
    """

    def get(self, task_id) -> dict:
        task = celery_app.AsyncResult(task_id)
        print(task.status)
        result = {"task_status": task.status}
        return result
