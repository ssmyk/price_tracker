from api import create_api


if __name__ == "__main__":
    scraper_api = create_api()
    scraper_api.run(host="0.0.0.0", port=5500, debug=True)