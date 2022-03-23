import celery.result
from flask import request
from flask.views import MethodView
from .scraper import scraper_task
#from scraper_app.tasks.scraper import scraper_task

class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'])
        #scraper_task.delay()
        return {"task_id":task.id}

class TasksStatus(MethodView):
    def get(self,task_id):
        task_result = celery.result.AsyncResult(task_id)
        result = {'task_id':task_id,'task_status':task_result.status,'task_result':task_result.result}
        return result
