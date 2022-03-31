from celery.utils.log import get_task_logger
from flask import request
from flask.views import MethodView
from celery.result import AsyncResult

from .scraper import scraper_task,celery_app

get_task_logger = get_task_logger(__name__)

#from api.scraper import scraper_task

class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'],body['user_id'])
        print(task.id)
        #task_result = task.result.AsyncResult(task_id)


        return {"task_id":task.id}

        #return {'task_id': task.id, 'task_status': task_result.status, 'task_result': task_result.result}
        #return {'task_status': task.status}
        #return task := scraper_task.delay(body['asin'])

'''
    def get(self):
        response = make_response()
        #response = jsonify(some='data')
        response.headers["Content-Type"] = "application/json"
        response.headers.add('Access-Control-Allow-Origin', '*')
        # return {"task_id":task.id}
        return response
'''
class TasksStatus(MethodView):
    def get(self,task_id):
        task = celery_app.AsyncResult(task_id)
        #get_task_logger.info(task)
        result = {'task_result':task.status}

        print(result)
        #result = task_status.result
        #result = {'task_id': task_id, 'task_status': task_result.status, 'task_result': task_result.result}
        return result
