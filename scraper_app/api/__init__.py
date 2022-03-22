from flask import Flask
from flask_cors import CORS

def create_api():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})

    from .views import ScraperAPI
    app.add_url_rule('/', view_func=ScraperAPI.as_view('scraper_api'), methods=['POST'])

    return app
