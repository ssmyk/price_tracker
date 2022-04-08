from bs4 import BeautifulSoup
import requests
from datetime import datetime
from celery import Celery
from celery.exceptions import Ignore

celery_app = Celery('tasks',backend='rpc://', broker='amqp://scraper:scraper@rabbitmq/scraper')
#celery_app = Celery('tasks', queue='scraper',backend='rpc://', broker='amqp://scraper:scraper@rabbitmq/scraper')
#celery_app = Celery('tasks',backend='rpc://', broker='amqp://guest:guest@rabbitmq//')

@celery_app.task(bind=True, default_retry_delay=1, max_retries=None)
def scraper_task(self, asin: str, user_id: str):
    page_url = f'https://www.amazon.pl/dp/{asin}'
    page = requests.get(page_url, timeout=None)
    if str(page) == "<Response [200]>":
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name = soup.title.string.split(':')[0]
        price = float(
            soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0', '').replace(',',
                                                                                                                '.'))
        image = soup.find(id="landingImage")['data-old-hires']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resp = requests.post('http://web_app:5000/products/', json={
            'product_name': product_name,
            'product_image': image,
            'product_asin': asin,
            'date_added': date,
            'current_price': price,
            'current_price_date': date,
            'lowest_price': price,
            'lowest_price_date': date,
            'fk_user': user_id})
        if resp.status_code == 409:
            self.update_state(state='DUPLICATE')
            raise Ignore()
        elif resp.status_code == 200:
            self.update_state(state='ADDED')
            raise Ignore()
        elif resp.status_code == 500:
            self.update_state(state='ERROR')
            raise Ignore()

    else:
        self.retry()

@celery_app.task(bind=True, default_retry_delay=1, max_retries=None)
def scraper_task_update(self, asin: str, user_id: str):
    page_url = f'https://www.amazon.pl/dp/{asin}'
    page = requests.get(page_url, timeout=None)
    if str(page) == "<Response [200]>":
        soup = BeautifulSoup(page.content, 'html.parser')
        price = float(
            soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0', '').replace(',',
                                                                                                                '.'))
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        requests.post('http://web_app:5000/products/update/', json={
            'product_asin': asin,
            'date': date,
            'price': price,
            'fk_user': user_id})
        return f'Current price for {asin}: {price} PLN'
    else:
        self.retry()

