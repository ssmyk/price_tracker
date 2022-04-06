import requests
from .scraper import scraper_task_update

def products_update():
    resp = requests.get('http://web_app:5000/products/')
    products = resp.json()
    for product in products:
        asin = product['product_asin']
        user_id = product['fk_user']
        scraper_task_update.delay(asin, user_id)
