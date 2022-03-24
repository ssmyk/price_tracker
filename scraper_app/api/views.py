from flask import request, make_response
from flask.views import MethodView

from worker.scraper import scraper_task


#from api.scraper import scraper_task

class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'])
        #task = scraper_task.delay()
        #scraper_task.delay()
        #response = make_response()
        # response = jsonify(some='data')
        #response.headers["Content-Type"] = "application/json"
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return {"task_id":task.id}
        #return task := scraper_task.delay(body['asin'])

'''
    def get(self):
        response = make_response()
        #response = jsonify(some='data')
        response.headers["Content-Type"] = "application/json"
        response.headers.add('Access-Control-Allow-Origin', '*')
        # return {"task_id":task.id}
        return response

class TasksStatus(MethodView):
    def get(self,task_id):
        task_result = celery.result.AsyncResult(task_id)
        result = {'task_id':task_id,'task_status':task_result.status,'task_result':task_result.result}
        return result
'''