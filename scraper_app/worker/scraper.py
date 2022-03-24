from bs4 import BeautifulSoup
import requests
from celery import Celery

tasks_app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@rabbitmq//')

class CallbackTask(tasks_app.Task):
    #def on_success(self, retval, task_id, args, kwargs):
        #w = AsyncResult(task_id)
     #   print(task_id)

    #def on_failure(self, exc, task_id, args, kwargs, einfo):
     #   self.retry()
     pass

@tasks_app.task(bind=True,base=CallbackTask,default_retry_delay=2,max_retries=None)
def scraper_task(self, asin: str):
    page_url = f'https://www.amazon.pl/dp/{asin}'
    #page_url = f'https://www.amazon.pl/dp/B08Q8L44GJ'
    print(page_url)
    page = requests.get(page_url, timeout=None)
    if str(page) == "<Response [200]>":
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name = soup.title.string.split(':')[0]
        price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0', '').replace(',','.'))
        image = soup.find(id="landingImage")['data-old-hires']
        return [product_name, price, image]
    else:
        print(page)
        self.retry()

