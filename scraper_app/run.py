from api import create_api
from flask_cors import CORS

if __name__ == "__main__":
    scraper_api = create_api()
    #cors = CORS(scraper_api, resources={r"/api/": {"origins": "http://localhost:5000"}})
    CORS(scraper_api)#, resources=r'/api/', headers='Content-Type', origins='*')
    #cors = CORS(scraper_api)
    #cors = CORS(scraper_api)#, resources={r"/api/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
    #scraper_api.config['CORS_HEADERS'] = 'Content-Type'
    scraper_api.run(host="0.0.0.0", port=5500, debug=True)
