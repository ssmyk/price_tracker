from bs4 import BeautifulSoup
import requests
from datetime import datetime
from celery import Celery



celery_app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@rabbitmq//')

class CallbackTask(celery_app.Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass
        #print(task_id)
        #w = AsyncResult(task_id)
        '''
        requests.post('http://web_app:5000/products/', json={
            'product_name': 'result',
            'product_asin': '212CSR0JE3G',
            'date_added': '2021-12-12 13:24:22',
            'current_price': '2394.43',
            'current_price_date': '2021-12-12 13:24:22',
            'lowest_price': '2100.12',
            'lowest_price_date': '2021-12-12 13:24:22',
            'fk_user': '1'})
        #print(task_id)
        '''
    #def on_failure(self, exc, task_id, args, kwargs, einfo):
     #   self.retry()


@celery_app.task(bind=True,base=CallbackTask,default_retry_delay=1,max_retries=None)
def scraper_task(self, asin: str, user_id: str):
    page_url = f'https://www.amazon.pl/dp/{asin}'
    #page_url = f'https://www.amazon.pl/dp/B08Q8L44GJ'
    print(page_url)
    page = requests.get(page_url, timeout=None)
    if str(page) == "<Response [200]>":
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name = soup.title.string.split(':')[0]
        price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0', '').replace(',','.'))
        image = soup.find(id="landingImage")['data-old-hires']

        resp = requests.post('http://web_app:5000/products/', json={
            'product_name': product_name,
            'product_image' : image,
            'product_asin': asin,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'current_price': price,
            'current_price_date': '2000-12-12 13:24:22',
            'lowest_price': '210.12',
            'lowest_price_date': '2000-12-12 13:24:22',
            'fk_user': user_id})
        return resp
    else:
        #print(page)
        self.retry()

