from celery import Celery, shared_task
import time
from bs4 import BeautifulSoup
from celery.result import AsyncResult
import requests

app = Celery('tasks',backend='rpc://',broker='amqp://guest:guest@localhost//')

@app.task
def add(x,y):
    time.sleep(5)
    return x+y

@app.task
def prod(asin: str):
    page_url = f'https://www.amazon.pl/dp/{asin}'
    page = requests.get(page_url, timeout=None)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_name = soup.title.string.split(':')[0]
    price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0','').replace(',','.'))
    image = soup.find(id="landingImage")['data-old-hires']
    return [product_name,price,image]
'''
@app.task(bind=True)
def pr(self):

    try:
        page_url = 'https://www.amazon.pl/UGEARS-Flexi-Cubus-antystresowe-koncentracj%C4%99/dp/B07BYD5MG2'
        page = requests.get(page_url, timeout=None)
    except:
        raise self.retry()
    soup = BeautifulSoup(page.content, 'html.parser')
    product_name = soup.title.string.split(':')[0]
    price = float(soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0','').replace(',','.'))
    image = soup.find(id="landingImage")['data-old-hires']
    return [product_name,price,image]
'''
class CallbackTask(app.Task):
    #def on_success(self, retval, task_id, args, kwargs):
        #w = AsyncResult(task_id)
     #   print(task_id)

    #def on_failure(self, exc, task_id, args, kwargs, einfo):
     #   self.retry()
     pass



@app.task(bind=True,base=CallbackTask,default_retry_delay=2,max_retries=None)  # this does the trick,retry_backoff=True
def p(self):
    page_url = 'https://www.amazon.pl/UGEARS-Flexi-Cubus-antystresowe-koncentracj%C4%99/dp/B07BYD5MG2'
    page = requests.get(page_url, timeout=None)
    if str(page) == "<Response [200]>":
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name = soup.title.string.split(':')[0]
        price = float(
        soup.find(id='tp_price_block_total_price_ww').get_text().split('zł')[0].replace('\xa0', '').replace(',', '.'))
        image = soup.find(id="landingImage")['data-old-hires']
        return [product_name, price, image]
    else:
        print(page)
        self.retry()