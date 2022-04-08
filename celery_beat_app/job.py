from app import celery_app
import requests

@celery_app.task(default_retry_delay=1, max_retries=None)
def run_update():
    requests.get('http://scraper_api:5500/api/')