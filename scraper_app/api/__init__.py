from flask import Flask

#import config

def create_api():
    app = Flask(__name__)

    from .views import ScraperAPI, TasksStatus
    app.add_url_rule('/', view_func=ScraperAPI.as_view('scraper_api'), methods=['POST'])
    app.add_url_rule('/status/<task_id>', view_func=TasksStatus.as_view('status'), methods=['GET'])

    return app
