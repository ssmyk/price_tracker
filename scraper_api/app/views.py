from flask import request
from flask.views import MethodView


from .scraper import scraper_task


#from api.scraper import scraper_task

class ScraperAPI(MethodView):
    def post(self):
        body = request.json
        print(body)
        print(body['asin'])
        task = scraper_task.delay(body['asin'])
        print(task.id)
        #task_result = task.result.AsyncResult(task_id)


        return {"task_id":task.id}
        #return {'task_id': task.id, 'task_status': task_result.status, 'task_result': task_result.result}
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
        task_result = celery.result.AsyncResult(task_id)
        result = {'task_id':task_id,'task_status':task_result.status,'task_result':task_result.result}
        return result
