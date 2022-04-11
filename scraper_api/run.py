from app import create_api
from flask_cors import CORS

if __name__ == "__main__":
    scraper_api = create_api()
    CORS(
        scraper_api,
        resources={r"/api/|/status/*": {"origins": "http://localhost:5000"}},
    )
    scraper_api.run(host="0.0.0.0", port=5500, debug=True)
